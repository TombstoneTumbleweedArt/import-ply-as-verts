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

# ########## Import PLY as Verts ########
#
# This module is close to 90% the original code supplied with Blender as the stock PLY import addon.  I have attempted
# to change it as little as possible and still obtain the desired result. 
#
# All love and respect to the original programmers who did all the heavy lifting for me :) 
#
# ##########


# ######### CHANGELOG ######## 
#
# v1.01 - "The Brad Patch": Added additional if clause to allow for unorthodox JWF ply files that contain odd
#           data similar to pscale and intensity
#           TODO:  Move this fix into the parser module so as to better strip out weird properties


'''
bl_info = {
    "name": "Import PLY as Verts",
    "author": "Michael A Prostka",
    "blender": (3, 1, 0),
    "location": "File > Import/Export",
    "description": "Import PLY mesh data as point cloud",
    "category": "Import-Export",
}
'''
from pickle import FALSE


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
        return [x.load(format, stream) for x in self.properties]

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
                    if not (len(s) >= 2 and s.startswith(b'"') and s.endswith(b'"')):
                        print("Invalid string", s)
                        print("Note: ply_import.py does not handle whitespace in strings")
                        return None
                    ans.append(s[1:-1])
                stream[:count] = []
                return ans
            if num_type == 'f' or num_type == 'd':
                mapper = float
            else:
                mapper = int
            ans = [mapper(x) for x in stream[:count]]
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


def read(filepath):
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
        if signature[3] != ord(b'\n'):
            if signature[3] != ord(b'\r'):
                print("Unknown line separator")
                return invalid_ply
            if signature[4] == ord(b'\n'):
                custom_line_sep = b"\r\n"
            else:
                custom_line_sep = b"\r"
                
        # Feb 15, 2022: Added rule for '\n\r' to pacify BTracer2 nonstandard ply         
        if signature[4] != ord(b'\r'):
                print("Unknown line separator")
                return invalid_ply
        else:
                custom_line_sep = b"\n\r"
        ########

        # Work around binary file reading only accepting "\n" as line separator.

        # TODO:     Apply the BTracer2 fix above to this module.  Not a huge priority as binary-encoded
        #                  \n\r PLY files are rare in the wild.
            
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
                            # Since reader code might (will) break iteration at this point,
                            # we have to ensure file is read up to here, yield, amd return...
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
                    obj_spec.specs[-1].properties.append(PropertySpec(tokens[4], type_specs[tokens[2]], type_specs[tokens[3]]))
                else:
                    obj_spec.specs[-1].properties.append(PropertySpec(tokens[2], None, type_specs[tokens[1]]))
        if not valid_header:
            print("Invalid header ('end_header' line not found!)")
            return invalid_ply

        obj = obj_spec.load(format_specs[format], plyf)

    return obj_spec, obj, texture

def load_ply_verts():
    print("Inside load_ply_verts()")
    pass

def load_ply_mesh(filepath, ply_name):
    import bpy

    obj_spec, obj, texture = read(filepath)
    # XXX28: use texture
    if obj is None:
        print("Invalid file")
        return

    uvindices = colindices = None
    colmultiply = None
    normals = False
    jwf = False
    '''
    if use_verts:
        print("Verts-> True")
    else:
        print("Verts-> False")
        '''
    # Read the file
    for el in obj_spec.specs:
        if el.name == b'vertex':
            vindices_x, vindices_y, vindices_z = el.index(b'x'), el.index(b'y'), el.index(b'z')
            uvindices = (el.index(b's'), el.index(b't'))
            if -1 in uvindices:
                uvindices = None
            # ignore alpha if not present
            if el.index(b'alpha') == -1:
                colindices = el.index(b'red'), el.index(b'green'), el.index(b'blue')
            else:
                colindices = el.index(b'red'), el.index(b'green'), el.index(b'blue'), el.index(b'alpha')
            if -1 in colindices:
                if any(idx > -1 for idx in colindices):
                    print("Warning: At least one obligatory color channel is missing, ignoring vertex colors.")
                colindices = None
            else:  # if not a float assume uchar
                colmultiply = [1.0 if el.properties[i].numeric_type in {'f', 'd'} else (1.0 / 255.0) for i in colindices]

        #elif el.name == b'face':
            #findex = el.index(b'vertex_indices')
        #elif el.name == b'tristrips':
          #  trindex = el.index(b'vertex_indices')
        #elif el.name == b'edge':
            #eindex1, eindex2 = el.index(b'vertex1'), el.index(b'vertex2')

    #mesh_faces = []
    mesh_uvs = []
    mesh_colors = []
    
    verts = obj[b'vertex']
    
    ################## ITS ALL IN THE verts OBJECT 
    # [0] = x pos
    # [1] = y pos
    # [2] = z pos
    # [3] = x norm      * If present
    # [4] = y norm
    # [5] = z norm
    # [6] = r color     * Will start at [3] if no normals found
    # [7] = g color
    # [8] = b color
    # [9] = a color
    
    # If len(verts[0]) is greater than 7, we have normals
    vertlength = len(verts[0])
    
    # BRAD PATCH - allow for JWF's len(9) files
    #
    # Needs a more elegant solution but this will band-aid for now
    
    if vertlength > 7:
        if vertlength < 10:
            jwf = True
        else:
            normals = True
    
    # Copy the positions
    mesh = bpy.data.meshes.new(name=ply_name)
    mesh.vertices.add(len(obj[b'vertex']))
    mesh.vertices.foreach_set("co", [a for v in obj[b'vertex'] for a in (v[vindices_x], v[vindices_y], v[vindices_z])])

    # Create our new object here
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    obj = bpy.data.objects.new(ply_name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
  
    # If colors are found, create a new Attribute 'Col' to hold them (NOT the Vertex_Color block!)
    
    if colindices: 
        # Create new Attribute 'Col' to hold the color data
        bpy.context.active_object.data.attributes.new(name="Col", type='FLOAT_COLOR', domain='POINT')
        newcolor = bpy.context.active_object.data
        # If there are no normals, the color data will start at [3], otherwise [6]
        for i, col in enumerate(verts):
            if normals == False:
                if len(colindices) == 3:
                    newcolor.attributes['Col'].data[i].color[0] = (verts[i][3]) / 255.0
                    newcolor.attributes['Col'].data[i].color[1] = (verts[i][4]) / 255.0
                    newcolor.attributes['Col'].data[i].color[2] = (verts[i][5]) / 255.0
                else: 
                    newcolor.attributes['Col'].data[i].color[0] = (verts[i][3]) / 255.0
                    newcolor.attributes['Col'].data[i].color[1] = (verts[i][4]) / 255.0
                    newcolor.attributes['Col'].data[i].color[2] = (verts[i][5]) / 255.0
                    newcolor.attributes['Col'].data[i].color[3] = (verts[i][6]) / 255.0
            elif normals == True:        
                if len(colindices) == 3:
                    newcolor.attributes['Col'].data[i].color[0] = (verts[i][6]) / 255.0
                    newcolor.attributes['Col'].data[i].color[1] = (verts[i][7]) / 255.0
                    newcolor.attributes['Col'].data[i].color[2] = (verts[i][8]) / 255.0
                else: 
                    newcolor.attributes['Col'].data[i].color[0] = (verts[i][6]) / 255.0
                    newcolor.attributes['Col'].data[i].color[1] = (verts[i][7]) / 255.0
                    newcolor.attributes['Col'].data[i].color[2] = (verts[i][8]) / 255.0
                    newcolor.attributes['Col'].data[i].color[3] = (verts[i][9]) / 255.0
            elif jwf == True:
                if len(colindices) == 3:
                    newcolor.attributes['Col'].data[i].color[0] = (verts[i][3]) / 255.0
                    newcolor.attributes['Col'].data[i].color[1] = (verts[i][4]) / 255.0
                    newcolor.attributes['Col'].data[i].color[2] = (verts[i][5]) / 255.0
                else: 
                    newcolor.attributes['Col'].data[i].color[0] = (verts[i][3]) / 255.0
                    newcolor.attributes['Col'].data[i].color[1] = (verts[i][4]) / 255.0
                    newcolor.attributes['Col'].data[i].color[2] = (verts[i][5]) / 255.0
                    newcolor.attributes['Col'].data[i].color[3] = (verts[i][6]) / 255.0
            
    mesh.update()
    mesh.validate()

    # Left from stock importer
    if texture and uvindices:
        pass
        # TODO add support for using texture.

        # import os
        # import sys
        # from bpy_extras.image_utils import load_image

        # encoding = sys.getfilesystemencoding()
        # encoded_texture = texture.decode(encoding=encoding)
        # name = bpy.path.display_name_from_filepath(texture)
        # image = load_image(encoded_texture, os.path.dirname(filepath), recursive=True, place_holder=True)

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


def load_ply(filepath):
    import time
    import bpy
   # import numpy

    t = time.time()
    ply_name = bpy.path.display_name_from_filepath(filepath)
 
    mesh = load_ply_mesh(filepath, ply_name)
    if not mesh:
        return {'CANCELLED'}

    print("\nSuccessfully imported %r in %.3f sec" % (filepath, time.time() - t))

    return {'FINISHED'}


def load(operator, context, filepath=""):
    return load_ply(filepath)