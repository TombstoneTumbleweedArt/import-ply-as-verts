# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>
'''
 Import PLY as Verts
 Up to the 3.0 Release, this module was close to 90% original Blender
 stock PLY import addon. With the changes introduced by Ms. Jarvis
 it no longer resembles the 2004 Python of that era, and the new
 functionality places it into a new weight class.

 Still all love and respect to the original programmers. :)

CHANGELOG

 v3.0 - The Jarvis Merge! Improved enough to justify a new version number.
        Now reads in header file and creates named attributes based on
        ply file header.

 v2.1 - Refactored the Brad Patch to theoretically accept any sort of weird
        ply file by only extracting the named color data (rgb[a]) from
        colindices.

 v2.0 - Reintegrated the original importer and added Verts/Colors as load
        option. Now correctly loads:

        MB3D BTracer Point Cloud PLY (v1.99 and earlier)
        MB3D BTracer2 PLY (v1.99.12 and later)
        JWF  Point Cloud
        Photogrammetry and other generic PLY containing at least vertex and
        color data

 v1.01 - "The Brad Patch": Added additional if clause to allow for unorthodox
        JWF ply files that contain odd data similar to pscale and intensity

bl_info = {
    "name": "Import PLY as Verts",
    "author": "Michael A Prostka, Katherine Jarvis",
    "blender": (3, 1, 0),
    "location": "File > Import/Export",
    "description": "Import PLY data with Attributes",
    "category": "Import-Export",
}
'''


class ElementSpec:
    __slots__ = (
        "name",
        "count",
        "properties",
    )

    def __init__(self, name, count):
        self.name = name
        self.count = count
        self.properties = []

    def load(self, format, stream):
        if format == b'ascii':
            stream = stream.readline().split()
        properties = self.properties
        return [x.load(format, stream) for x in properties]

    def index(self, name):
        for i, p in enumerate(self.properties):
            if p.name == name:
                return i
        return -1


class PropertySpec:
    __slots__ = (
        "name",
        "list_type",
        "numeric_type",
    )

    def __init__(self, name, list_type, numeric_type):
        self.name = name
        self.list_type = list_type
        self.numeric_type = numeric_type

    def read_format(self, format, count, num_type, stream):
        import struct

        if format == b'ascii':
            if num_type == 's':
                ans = []
                for i in range(count):
                    s = stream[i]
                    if not (len(s) >= 2 and s.startswith(b'"') and
                            s.endswith(b'"')):
                        print("Invalid string", s)
                        print(
                            "Note: ply_import.py does not handle"
                            "whitespace in strings")
                        return None
                    ans.append(s[1:-1])
                stream[:count] = []
                return ans
            if num_type == 'f' or num_type == 'd':
                mapper = float
            else:
                mapper = int
            ans = [mapper(x) for x in stream[:count]]
            # pop the buffer stack
            stream[:count] = []
            return ans
        else:
            if num_type == 's':
                ans = []
                for i in range(count):
                    fmt = format + 'i'
                    data = stream.read(struct.calcsize(fmt))
                    length = struct.unpack(fmt, data)[0]
                    fmt = '%s%is' % (format, length)
                    data = stream.read(struct.calcsize(fmt))
                    s = struct.unpack(fmt, data)[0]
                    ans.append(s[:-1])  # strip the NULL
                return ans
            else:
                fmt = '%s%i%s' % (format, count, num_type)
                data = stream.read(struct.calcsize(fmt))
                return struct.unpack(fmt, data)

    def load(self, format, stream):
        if self.list_type is not None:
            count = int(self.read_format(format, 1, self.list_type, stream)[0])
            return self.read_format(format, count, self.numeric_type, stream)
        else:
            return self.read_format(format, 1, self.numeric_type, stream)[0]


class ObjectSpec:
    __slots__ = ("specs",)

    def __init__(self):
        # A list of element_specs
        self.specs = []

    def load(self, format, stream):
        return {
            i.name: [
                i.load(format, stream) for j in range(i.count)
            ]
            for i in self.specs
        }


def read_header(self, filepath):
    import bpy
    import re

    format = b''
    texture = b''
    version = b'1.0'
    format_specs = {
        b'binary_little_endian': '<',
        b'binary_big_endian': '>',
        b'ascii': b'ascii',
    }
    type_specs = {
        b'char': 'b',
        b'uchar': 'B',
        b'int8': 'b',
        b'uint8': 'B',
        b'int16': 'h',
        b'uint16': 'H',
        b'short': 'h',
        b'ushort': 'H',
        b'int': 'i',
        b'int32': 'i',
        b'uint': 'I',
        b'uint32': 'I',
        b'float': 'f',
        b'float32': 'f',
        b'float64': 'd',
        b'double': 'd',
        b'string': 's',
    }
    obj_spec = ObjectSpec()
    invalid_ply = (None, None, None)
    with open(filepath, 'rb') as plyf:
        signature = plyf.peek(5)

        if not signature.startswith(b'ply') or not len(signature) >= 5:
            print("Signature line was invalid")
            return invalid_ply

        custom_line_sep = None
        #  Allow for the following patterns:
        #              CRLF (MB3D)  LFCR (BTracer2)     Binary / ASCII LF only
        #   ASCII      1310         1013                10
        #   Python     \r\n         \n\r                \n

        # CRLF
        if signature[3] != ord(b'\n'):
            if signature[3] != ord(b'\r'):
                print("Unknown line separator")
                return invalid_ply
            if signature[4] == ord(b'\n'):
                custom_line_sep = b"\r\n"
            else:
                custom_line_sep = b"\r"

        # The Others
        if signature[3] == ord(b'\n'):
            if custom_line_sep is None:
                # If no \r (ie LF only) present, force one
                if signature[4] != ord(b'\r'):
                    custom_line_sep = b'\n'
                else:
                    custom_line_sep = b"\n\r"

        # The Jarvis Parser™, Part 1
        # Detects ALL property entries in the Header and
        # extracts the literal name(s)

        if custom_line_sep is None:  # header split up by lines
            lines = re.split(b'\n', signature)
        else:
            lines = x = re.split(custom_line_sep, signature)

        # turn into a binary regexp
        keys = list(type_specs.keys())
        keys_str = str(keys)
        keys_str = keys_str.replace(", ", "|")
        keys_str = keys_str.replace("b'", "")
        keys_glue = keys_str.replace("'", "")

        prog = re.compile(b'^property ' + bytes(keys_glue, 'utf-8') + b'+ ')
        # MP - added 'and not' clause to omit vertex index list
        matches = [
                match for match in lines if match.startswith(b'property')
                and not match.startswith(b'property list')
                ]
        # lines that start with word property
        properties = []
        for it_ind in range(len(matches)):
            properties.append([])
            eraser = prog.findall(matches[it_ind])[0]
        # what we want to remove (everything but property name)
            properties[it_ind] = matches[it_ind].replace(eraser, b'')
            properties[it_ind] = properties[it_ind].replace(b" ", b'')
        # reduce to just name of property and store in a list

        # Work around binary file reading only accepting
        # "\n" as line separator.
        # The below line causes pep8 code e731 (Original Comment)
        plyf_header_line_iterator = lambda plyf: plyf
        if custom_line_sep is not None:
            def _plyf_header_line_iterator(plyf):
                buff = plyf.peek(2**16)
                while len(buff) != 0:
                    read_bytes = 0
                    buff = buff.split(custom_line_sep)
                    for line in buff[:-1]:
                        read_bytes += len(line) + len(custom_line_sep)
                        if line.startswith(b'end_header'):
                            # Since reader code might (will) break iteration
                            # at this point, we have to ensure file is read
                            # up to here, yield, amd return...
                            plyf.read(read_bytes)
                            yield line
                            return
                        yield line
                    plyf.read(read_bytes)
                    buff = buff[-1] + plyf.peek(2**16)
            plyf_header_line_iterator = _plyf_header_line_iterator

        valid_header = False
        for line in plyf_header_line_iterator(plyf):
            tokens = re.split(br'[ \r\n]+', line)

            if len(tokens) == 0:
                continue
            if tokens[0] == b'end_header':
                valid_header = True
                break
            elif tokens[0] == b'comment':
                if len(tokens) < 2:
                    continue
                elif tokens[1] == b'TextureFile':
                    if len(tokens) < 4:
                        print("Invalid texture line")
                    else:
                        texture = tokens[2]
                continue

            elif tokens[0] == b'obj_info':
                continue
            elif tokens[0] == b'format':
                if len(tokens) < 3:
                    print("Invalid format line")
                    return invalid_ply
                if tokens[1] not in format_specs:
                    print("Unknown format", tokens[1])
                    return invalid_ply
                try:
                    version_test = float(tokens[2])
                except Exception as ex:
                    print("Unknown version", ex)
                    version_test = None
                if version_test != float(version):
                    print("Unknown version", tokens[2])
                    return invalid_ply
                del version_test
                format = tokens[1]

            elif tokens[0] == b'element':
                if len(tokens) < 3:
                    print("Invalid element line")
                    return invalid_ply
                obj_spec.specs.append(ElementSpec(tokens[1], int(tokens[2])))

            elif tokens[0] == b'property':
                if not len(obj_spec.specs):
                    print("Property without element")
                    return invalid_ply
                if tokens[1] == b'list':
                    last_spec = obj_spec.specs[-1]
                    property = PropertySpec(tokens[4],
                                            type_specs[tokens[2]],
                                            type_specs[tokens[3]]
                                            )
                    last_spec.properties.append(property)
                else:
                    last_spec = obj_spec.specs[-1]
                    property = PropertySpec(tokens[2],
                                            None,
                                            type_specs[tokens[1]]
                                            )
                    last_spec.properties.append(property)

        if not valid_header:
            print("Invalid header ('end_header' line not found!)")
            return invalid_ply

        use_faces = False

        # HEADER INFO
        # This convoluted bit of boolean karate was deemed necessary to
        # detect if a user is attempting to load a point cloud as a
        # triangle mesh, while also allowing triangle meshes to be loaded
        # as either cloud or mesh.
        for spec in obj_spec.specs:
            if spec.name == b'vertex':
                print(f'Vertices-> {spec.count}')
            if spec.name == b'face' and spec.count < 1:
                print(f'Faces-> {spec.count}')
            # 'element face 0' in file (JWF, we see you!)
                self.use_verts = True
                use_faces = False
            # Triangle mesh as cloud
            if (spec.name == b'face' and
                    spec.count > 1 and
                    self.use_verts is True):
                use_faces = False
            # Triangle mesh as triangles
            if (spec.name == b'face' and
                    spec.count > 1 and
                    self.use_verts is False):
                use_faces = True

        if use_faces:
            self.use_verts = False
        else:
            self.use_verts = True

        print(properties)
        print("Header has been parsed.")
        print("Loading data...")

        # BOTTLENECK #1 - raw data load needs massive optimization etc.
        obj = obj_spec.load(format_specs[format], plyf)

    return obj, obj_spec, properties, texture


def get_properties(properties, colindices, el):
    stand_props = [b'x', b'y', b'z', b'red', b'green', b'blue', b'alpha']
    # standard properties list
    not_standard = list(set(properties) - set(stand_props))
    # the result has to be a list of strings
    weirdind = []
    rgb = (b'red', b'green', b'blue')
    rgba = (b'red', b'green', b'blue', b'alpha')
    if any(color in s.lower() for color in (rgba)
            for s in properties):
        colindices = (el.index(b'red'), el.index(b'green'),
                      el.index(b'blue'), el.index(b'alpha'))
    elif any(color in s.lower() for color in (rgb)
             for s in properties):
        colindices = el.index(b'red'), el.index(b'green'), el.index(b'blue')

    if not_standard:
        for loop_ind in range(len(not_standard)):
            weirdind.append(el.index(not_standard[loop_ind]))
    # gives us locations of other attributes within the list

    print(f'WeirdInd -> {weirdind} | NS -> {not_standard}')
    return not_standard, weirdind, colindices


def load_ply_mesh(obj_spec, obj, texture, properties, ply_name):
    import bpy
    import numpy as np
    print("Building mesh...")

    # XXX28: use texture
    uvindices = colindices = None
    colmultiply = None

    # MP Comment - below comments are left from stock importer
    # TODO import normals
    # noindices = None

    for el in obj_spec.specs:
        if el.name == b'vertex':
            weirdind = []  # create weirdind list, with length of zero
            vindices_x = el.index(b'x')
            vindices_y = el.index(b'y')
            vindices_z = el.index(b'z')
            # noindices = (el.index('nx'), el.index('ny'), el.index('nz'))
            # if -1 in noindices: noindices = None
            uvindices = (el.index(b's'), el.index(b't'))
            if -1 in uvindices:
                uvindices = None

    # The Jarvis Parser™, Part 2
            if len(properties) > 3:  # more than just x, y, and z
                not_standard, weirdind, colindices = get_properties(
                    properties, colindices, el)
            # ignore alpha if not present
            if el.index(b'alpha') == -1:
                colindices = (el.index(b'red'), el.index(b'green'),
                              el.index(b'blue'))
            else:
                colindices = (el.index(b'red'), el.index(b'green'),
                              el.index(b'blue'), el.index(b'alpha'))
            if -1 in colindices:
                if any(idx > -1 for idx in colindices):
                    print("Warning: At least one obligatory color channel is"
                          "missing, ignoring vertex colors.")
                colindices = None
            else:  # if not a float assume uchar
                colmultiply = [
                    1.0 if el.properties[i].numeric_type in {'f', 'd'}
                    else (1.0 / 255.0) for i in colindices
                ]
        elif el.name == b'face':
            findex = el.index(b'vertex_indices')
        elif el.name == b'tristrips':
            trindex = el.index(b'vertex_indices')
        elif el.name == b'edge':
            eindex1, eindex2 = el.index(b'vertex1'), el.index(b'vertex2')

    mesh_faces = []
    mesh_uvs = []
    mesh_colors = []

    # MP Note - Meshes still use the old style Face Corner -> Byte Color.
    # Will eventually update this to the newer Vertex Color data type
    def add_face(vertices, indices, uvindices, colindices):
        mesh_faces.append(indices)
        if uvindices:
            mesh_uvs.extend([
                (vertices[index][uvindices[0]], vertices[index][uvindices[1]])
                for index in indices
            ])
        if colindices:
            if len(colindices) == 3:
                mesh_colors.extend([
                    (
                        vertices[index][colindices[0]] * colmultiply[0],
                        vertices[index][colindices[1]] * colmultiply[1],
                        vertices[index][colindices[2]] * colmultiply[2],
                        1.0,
                    )
                    for index in indices
                ])
            elif len(colindices) == 4:
                mesh_colors.extend([
                    (
                        vertices[index][colindices[0]] * colmultiply[0],
                        vertices[index][colindices[1]] * colmultiply[1],
                        vertices[index][colindices[2]] * colmultiply[2],
                        vertices[index][colindices[3]] * colmultiply[3],
                    )
                    for index in indices
                ])

    if uvindices or colindices:
        # If we have Cols or UVs then we need to check the face order.
        add_face_simple = add_face

        # EVIL EEKADOODLE - face order annoyance.
        def add_face(vertices, indices, uvindices, colindices):
            if len(indices) == 4:
                if indices[2] == 0 or indices[3] == 0:
                    indices = indices[2], indices[3], indices[0], indices[1]
            elif len(indices) == 3:
                if indices[2] == 0:
                    indices = indices[1], indices[2], indices[0]

            add_face_simple(vertices, indices, uvindices, colindices)

    verts = obj[b'vertex']
    num_props = np.size(verts[0])

    if b'face' in obj:
        for f in obj[b'face']:
            ind = f[findex]
            add_face(verts, ind, uvindices, colindices)

    if b'tristrips' in obj:
        for t in obj[b'tristrips']:
            ind = t[trindex]
            len_ind = len(ind)
            for j in range(len_ind - 2):
                add_face(
                    verts,
                    (ind[j], ind[j + 1], ind[j + 2]),
                    uvindices,
                    colindices
                )
    mesh = bpy.data.meshes.new(name=ply_name)
    mesh.vertices.add(len(obj[b'vertex']))
    mesh.vertices.foreach_set(
        "co",
        [a for v in obj[b'vertex'] for a in (
            v[vindices_x],
            v[vindices_y],
            v[vindices_z])]
    )
    if b'edge' in obj:
        mesh.edges.add(len(obj[b'edge']))
        mesh.edges.foreach_set(
            "vertices",
            [a for e in obj[b'edge'] for a in (e[eindex1], e[eindex2])]
        )

    if mesh_faces:
        loops_vert_idx = []
        faces_loop_start = []
        faces_loop_total = []
        lidx = 0
        for f in mesh_faces:
            nbr_vidx = len(f)
            loops_vert_idx.extend(f)
            faces_loop_start.append(lidx)
            faces_loop_total.append(nbr_vidx)
            lidx += nbr_vidx

        mesh.loops.add(len(loops_vert_idx))
        mesh.polygons.add(len(mesh_faces))

        mesh.loops.foreach_set("vertex_index", loops_vert_idx)
        mesh.polygons.foreach_set("loop_start", faces_loop_start)
        mesh.polygons.foreach_set("loop_total", faces_loop_total)

        if uvindices:
            uv_layer = mesh.uv_layers.new()
            for i, uv in enumerate(uv_layer.data):
                uv.uv = mesh_uvs[i]

        if colindices:
            vcol_lay = mesh.vertex_colors.new()
            for i, col in enumerate(vcol_lay.data):
                col.color[0] = mesh_colors[i][0]
                col.color[1] = mesh_colors[i][1]
                col.color[2] = mesh_colors[i][2]
                col.color[3] = mesh_colors[i][3]

    # Create our new object here
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    obj = bpy.data.objects.new(ply_name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    numverts = np.size(verts, 0)
    print("Mesh Built")

    # The Jarvis Parser™, Part 3a Triangle Mesh with Attributes

    newattribute = bpy.context.active_object.data  # renamed from newcolor
    color_indices = colindices
    if weirdind:  # create custom variable names
        for j, item in enumerate(weirdind):
            newattribute.attributes.new(
                name=str(not_standard[j], 'utf-8'),
                type='FLOAT',
                domain='POINT'
            )
    if colindices and weirdind:
        for i in range(numverts):
            for j in range(len(weirdind)):
                newattribute.attributes[
                    str(not_standard[j], 'utf-8')
                ].data[i].value = (verts[i][weirdind[j]])
    elif weirdind:  # no colors but still custom attributes
        for i in range(numverts):
            for j in range(len(weirdind)):
                newattribute.attributes[
                    str(not_standard[j], 'utf-8')
                ].data[i].value = (verts[i][weirdind[j]])

    mesh.update()
    mesh.validate()

    if texture and uvindices:
        pass

        # MP NOTE - Comment left from original code

        # TODO add support for using texture.

        # import os
        # import sys
        # from bpy_extras.image_utils import load_image

        # encoding = sys.getfilesystemencoding()
        # encoded_texture = texture.decode(encoding=encoding)
        # name = bpy.path.display_name_from_filepath(texture)
        # image = load_image(encoded_texture, os.path.dirname(filepath),
        #           recursive=True, place_holder=True)

        # if image:
        #     texture = bpy.data.textures.new(name=name, type='IMAGE')
        #     texture.image = image

        #     material = bpy.data.materials.new(name=name)
        #     material.use_shadeless = True

        #     mtex = material.texture_slots.add()
        #     mtex.texture = texture
        #     mtex.texture_coords = 'UV'
        #     mtex.use_map_color_diffuse = True

        #     mesh.materials.append(material)
        #     for face in mesh.uv_textures[0].data:
        #         face.image = image
    return mesh


def load_ply_verts(obj_spec, obj, texture, properties, ply_name):
    import bpy
    import numpy as np

    uvindices = colindices = None
    colmultiply = None

    # Parse the data
    for el in obj_spec.specs:
        if el.name == b'vertex':
            weirdind = [] #create weirdind list, with length of zero
            vindices_x = el.index(b'x')
            vindices_y = el.index(b'y')
            vindices_z = el.index(b'z')
            uvindices = (el.index(b's'), el.index(b't'))
            if -1 in uvindices:
                uvindices = None
            
            # The Jarvis Parser™, Part 2
            if len(properties) > 3:  # more than just x, y, and z
                not_standard, weirdind, colindices = get_properties(
                    properties, colindices, el)
    mesh_uvs = []
    mesh_colors = []
    verts = obj[b'vertex']
    num_props=np.size(verts[0])
    
    # Copy the positions
    mesh = bpy.data.meshes.new(name=ply_name)
    mesh.vertices.add(len(obj[b'vertex']))
    mesh.vertices.foreach_set(
        "co",
        [a for v in obj[b'vertex'] for a in (
            v[vindices_x],
            v[vindices_y],
            v[vindices_z])]
    )
    # Create our new object here
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    obj = bpy.data.objects.new(ply_name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    numverts=np.size(verts,0)

    # The Jarvis Parser™, Part 3b - Point Cloud with Attributes
    newattribute = bpy.context.active_object.data # renamed from newcolor
    color_indices = colindices
    if weirdind:  # create custom variable names
        for j, item in enumerate(weirdind):
            newattribute.attributes.new(
                name=str(not_standard[j], 'utf-8'),
                type='FLOAT',
                domain='POINT'
            )

    if colindices and weirdind:
        newattribute.attributes.new(name="Col", type='FLOAT_COLOR', domain='POINT')  
        for i in range(numverts):    
            newattribute.attributes['Col'].data[i].color = [(verts[i][colindex]) / 255.0 for colindex in colindices]
            for j in range(len(weirdind)):
                    newattribute.attributes[str(not_standard[j],'utf-8')].data[i].value = (verts[i][weirdind[j]])           
    elif weirdind: # no colors but still custom attributes
        for i in range(numverts):
            for j in range(len(weirdind)):
                    newattribute.attributes[str(not_standard[j],'utf-8')].data[i].value = (verts[i][weirdind[j]])        
    elif colindices: #just colors, no custom attributes
        newattribute.attributes.new(name="Col", type='FLOAT_COLOR', domain='POINT')      
        for i in range(numverts):     
            newattribute.attributes['Col'].data[i].color = [(verts[i][colindex]) / 255.0 for colindex in colindices]  
              
    mesh.update()
    mesh.validate()

    # Left from stock importer
    if texture and uvindices:
        pass

    print("Vert Mesh built.")
    return mesh

def load_ply(self, filepath):
    import time
    import bpy

    t = time.time()
    ply_name = bpy.path.display_name_from_filepath(filepath)
    
    text_output = bpy.data.texts.new(f'IPAV: {ply_name}')
  
    obj, obj_spec, properties, texture = read_header(self, filepath)
    
    if obj is None:
        print("Invalid file")
        return
    
    for spec in obj_spec.specs:
        if spec.name == b'vertex':
            text_output.write(f'Vertices-> {spec.count}')
        if spec.name == b'face' and spec.count > 1:
            text_output.write(f'\nFaces-> {spec.count}')
    text_output.write(f'\nProperties: {", ".join(str(prop, "UTF-8") for prop in properties)}')
    
    if self.use_verts:
        print("Verts Only")
        mesh = load_ply_verts(obj_spec, obj, texture, properties, ply_name)
    else:
        print("Verts and Faces")
        mesh = load_ply_mesh(obj_spec, obj, texture, properties, ply_name)
 
    if not mesh:
        return {'CANCELLED'}
    
    text_output.write(f'\nImported: {ply_name} in {time.time() - t:.3f} sec')
    print("\nSuccessfully imported %r in %.3f sec" % (filepath, time.time() - t))

    return {'FINISHED'}


def load(operator, context, filepath=""):
    return load_ply(operator, filepath)
