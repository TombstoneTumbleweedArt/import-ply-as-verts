# import-ply-as-verts v3.0 &nbsp; &nbsp; &nbsp; &nbsp; [![Generic badge](https://img.shields.io/badge/Release-3.0-<COLOR>.svg)](https://shields.io/) &nbsp; &nbsp; &nbsp; &nbsp; ![Logo_Blender-Dark](https://user-images.githubusercontent.com/24717972/154959144-bd55fdc0-2ab9-43e4-8747-33c7465a9c8f.svg)    
## Blender Python PLY Import Addon

### Preamble
As of Blender 4.0 the original Python PLY import/export will be deprecated in favor of the new C++ modules.
These modules are a great deal faster (at the moment) but nowhere near as source-friendly as Python. 
Due to the flexible nature of the PLY format, compatibility with Blender has remained an issue. Our open-source
Python Addon is currently the most compatible and flexible option for nonstandard models such as point clouds.

### Our thanks to Ms. Katherine Jarvis, a true Pythonista.

### New to 3.0
__________________________________
<ul>
  <li><strong>Attributes.</strong> <strong><i>ALL</i></strong> data in the PLY file - vertex colors, normals, etc., is parsed into usable Blender Attributes.
  <li>Improved compatibility, especially with CloudCompare.</li>
  <li>Improved performance (more to come).</li>
  <li>The program is now an actual Addon and not the kludgey install hack from previous versions :) </li>
</ul>


 
# Why

- Attempting to import certain PLY files with Blender's stock importer will fail:
  
   - Triangle/Quad Meshes with nonstandard file terminators <i>(BTracer2 PLY export)</i>
   
   - Zero edge/face point cloud files, ie:
    
     - Mandelbulb3D BTracer Point Cloud <i>(v.1.99 and earlier)</i>
     - Mandelbulb3D BTracer2 PLY <i>(1.99.12 and later)</i>
     - J-Wildfire Point Cloud 
     - Photogrammetry scans  <i>(MeshLab, CloudCompare,</i> et. al.<i>)</i>
     - Practically any 'extra' value beyond xyz, vertex normal, and vertex color.


 The result in Blender a system console window error message or no error at all.    


> Legacy Python error message, Blender 3.6 and earlier:

   ![Error-Message](https://user-images.githubusercontent.com/24717972/154848070-c59145aa-8d9e-4000-8de8-077cd3ad11f1.jpg)


> C++ Import error message, Blender 3.6 and higher:

![image](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/de1c4ed7-c24b-493f-b459-2a5483934d63)




Prior to this, a fair workaround was to process the point cloud in MeshLab.  I love MeshLab and use it often. However, despite it being capable of importing a much wider variety of nonstandard PLY, MeshLab still strips out 'extra' data if the model is reexported. 

Ms. Katherine Jarvis of the <a href="https://hajim.rochester.edu/me/sites/sefkow/index.html">Triforce Institute for Multiphysics Modeling</a> needed to preserve additional simulation data.  Her generous contributions to the codebase in the form of the <strong>Jarvis Parser&#8482; *</strong> addresses that issue by neatly converting said data into Blender Attributes.

>  *(Not actually trademarked, but innovative enough I feel she deserves one :).


# Results


> <i>(Left to Right, Back Row First)</i>
>   - <strong>Vertex-Painted Suzanne</strong> <i>(Same file as Mesh and Verts)</i>; 
>   - <strong>BTracer2</strong> <i>(Same file as Mesh and Verts)</i>;  
>   - <strong>J-Wildfire Point Cloud</strong>; 
>   - <strong>Photogrammetry Point Cloud</strong>

![The_Gang](https://user-images.githubusercontent.com/24717972/154947983-be7a2e52-a9f8-4114-b887-8933970f96c7.jpg)

![The_Gang-Render](https://user-images.githubusercontent.com/24717972/154948015-238c3d0d-43e4-4b63-a316-4f4470ce172d.jpg)

All the objects in this scene share a single Material of correctly imported vertex colors. The point clouds have a simple Geometry Node tree applied . 

# Cycles Point Cloud Render
The Point Cloud Render mode in Cycles works beautifully well with these (thank you to <strong>Bone Studio</strong> and <strong>Daniel Leike</strong>).  A tutorial is available on <a href="https://www.youtube.com/watch?v=K5xH4T_qcec&t=1s">YouTube</a>, and our image was included in the <a href="https://wiki.blender.org/wiki/Reference/Release_Notes/3.1/Cycles">Blender 3.1 Release Notes - Cycles</a>

![31-Notes](https://user-images.githubusercontent.com/24717972/158804408-633a6bcf-fe94-416a-8e21-751b29687b2f.png)

# Compatibility
  - If your PLY won't work, contact me and we'll figure out why.
  - Best results will be had with Blender 3.1 or later (4.0 is verified).
  - Mesh Import is verified for 3.0 (thanks to <strong>Carisma Alex</strong> for asking!) and works exactly like the process in <a href="https://youtu.be/4u-kS9IeTc4">Mandelbulb3D - BTracer2 Workflow Basic</a>.  However, the Point Cloud object requires new functionality added in Blender 3.1 to correctly assign the colors.  Direct import results in a charcoal briquette with missing surface normals.  A workaround is to create the Point Cloud in 3.1 (with applied Geo Node Modifier), save as a .blend file or export to a modern format like .gltf, and open in 3.0.  A call to (Edit Mode) Mesh->Normals->Recalculate Outside is usually necessary.


       ![Compatibility-sm](https://user-images.githubusercontent.com/24717972/155842926-f474fc6e-603a-4fa0-a1de-553f35df85ca.jpg)
         



# Installation

 1. Download the `Import_PLY_as_Verts-3.zip` file from the repo.
 2. Unzip the file.
 3. Do <strong><i>NOT</i></strong> unzip the `PLY_As_Verts.zip` file.  That is the actual Addon.
 4. (Optional) Read <strong>The_Manual.</strong>  <i>It's quite good :)</i>
 5. Open Blender.  If using 3.6 or lower, disable the legacy PLY i/o modules:


![image3](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/c279e483-afe3-4283-a4ec-e0ce2ecfb6a4)

And if necessary, remove old versions of the Addon:

![Cap-0028](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/6bce4943-5493-4f9e-9658-80065c276b46)


  
 6. Install the new Addon. Make sure the checkbox is ticked.

![Cap-0031](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/76e678a3-5b17-455f-a043-b05d2bfbcea3)

  
 

# Usage

<i>File->Import</i> will now look like this:


![File_Screenshot](https://user-images.githubusercontent.com/24717972/154866087-3e15bcbc-8537-444c-af1d-4d41c4f25a36.jpg)

  
  Selecting <i>Stanford PLY as Verts</i> will bring up the Filebrowser as usual, with an additional checkbox:
  

![image6](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/2605253a-1cf8-49be-b6d6-c324ebaf2076)


Several things may happen at this point:
  - A triangle/quad mesh file may be loaded as either point cloud (checkbox selected) or mesh (checkbox deselected).
  - A point cloud file may be loaded with the checkbox selected.
  - A point cloud file may be loaded with the checkbox deselected, and the autodetect routine will use the correct loading method.
    

As your model is importing, statistics about it will be sent to Blender's <strong>Console Window.</strong>

![Cap-0035](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/649ed6ea-56a9-4b2d-a821-c45a5eff2eff)


However, said <strong>Console Window</strong> is not trivial to get to for non-Windows users.

As a remedy the Addon generates a text file inside of Blender's <strong>Text Editor.</strong>

![Cap-0036](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/74568daa-8bd5-4126-91a6-e057e9e0c1fe)

Once your model has loaded, two common workflows are:

### A) Cycles Point Cloud Render
In the Geometry Nodes Editor, create a new nodetree.
`Add-> Mesh-> Operations-> Mesh to Points` makes the cloud renderable (although <strong><i>NOT</i></strong> in Viewport Mode).


![image](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/6ed87b9a-29b2-4c42-9ba7-e24af69b01d6)
![Cap-0039-B](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/7911e822-6b86-41ea-b098-a7055824bf59)

Geometry, but no color.

In order to connect the imported Vertex Colors, first create a new Material.

Go to `Add-> Input-> Attributes-> Col` and connect the Node.
Name the Material something meaningful.

![Cap-0038](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/c7b7b515-ca85-40da-b9e1-90e7ff3d7aae)

Switch back to Geometry Nodes and `Add-> Material-> Set Material`.


Plug in the meaningful name you just bestowed upon the Material.


![Cap-0039](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/10b6c6d6-74b8-4f39-b399-507392eeee79)

![image17](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/fd52cb59-2d91-4626-8b89-859766487dce)

> <strong>MUCH</strong> better :)
> 
> More details are covered in The_Manual.

### B) Instancing
Another approach to visualization is to attach actual geometry to the points in the cloud.
This allows great flexibility at the cost of higher memory use.
However, unlike the Cycles workflow we just looked at, these do work in Viewport Render.

With this in mind, here is a basic Instancing setup:

In a new Geometry Nodes block, `Add-> Instances-> Instance on Points`


![image](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/881f9d79-1499-45d3-a84a-6f5f0be0c37d)


Nothing immediately happens because we have to supply some input geometry.

`Add-> Mesh-> Primitives-> Cube` and connect.

![image](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/6a0a61e5-9e51-4ba7-be3b-0fb9a2f28afb)
![image](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/e6d5c79c-c326-4408-828d-47f3aa4a404c)

The scale is usually off at the beginning, we'll fine-tune in a moment.

We see now we have 19.6K copies of the Cube as Instances.

![image](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/ee68b977-106c-4a03-96c9-c83ce56d20cb)

Instances tend to bog down as the geometry increases.

To speed things up, add a `Realize Instances` node.
Also drop the `Size` of our cube object to `0.02` meters.

![image](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/a48bfe18-7150-4af9-b32a-fe3b73f413f3)
![image](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/286b0716-1903-4ef1-8b80-4b097c69891b)


If you haven't already made a custom Material as discussed in the previous section, go ahead and do so.

When it's done, drop a `Set Material` node right after `Realize Instances` and name it.

![image24](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/18677cd9-d6c8-4b90-b87f-c05dfb2ce580)
![image25](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/7aa8ec6b-9314-41cd-bef0-91c78705bc70)
![image26](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts/assets/24717972/03377f57-c16d-497c-b472-daa0c6420a53)

> That is very attractive data.
>
> This and other topics are covered in greater detail in <strong>The_Manual</strong>.



# Python API
  
  The API call has a new optional Boolean parameter, `use_verts` (default=False):
  
   `bpy.ops.import_mesh.ply(filepath="", files=[], use_verts=False, directory="", filter_glob="*.ply")`
   
  and is used similar to
      
   `Dave = bpy.ops.import_mesh.ply(filepath="C:\\mb3d_mesh.ply", use_verts=True)`  
   
   <strong>Backward Compatibility</strong>
   
   A call like 
    ` Dave = bpy.ops.import_mesh.ply(filepath="C:\\mb3d_mesh.ply")` 
   is equivalent to using the legacy importer and <i>shouldn't</i> break existing scripts.
    
    
    
# Proposed API Docs

   `bpy.ops.import_mesh.ply(<i>filepath='', files=None, use_verts=False, directory='', filter_glob='*.ply'</i>)`
   
  > Load a PLY geometry file as verts or mesh with Attributes (if present)
    
      Parameters: filepath (string, (optional, never None)) – File Path, Filepath used for importing the file
                  files (bpy_prop_collection of OperatorFileListElement, (optional)) – File Path, File path used for importing the PLY file
                  use_verts (boolean, (optional)) - Load as verts or triangle/quad mesh
                  hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings
                  directory (string, (optional, never None)) – directory
                  filter_glob (string, (optional, never None)) – filter_glob
  
  >   File: addons/io_mesh_ply/__init__.py:81


# Roadmap

   - Performance can still be improved. The worst bottleneck is loading Blender's data structures. This is under investigation.
   - Exporting Blender objects as verts is not yet supported.  Not a huge priority but will be addressed.
   
    
# Tutorials
  
## Note: These are a bit dated but essentially the same.  Newer videos are in the works.
  1. <a href="https://youtu.be/4u-kS9IeTc4">Mandelbulb3D - BTracer2 Workflow Basic</a>
  2. <a href="https://youtu.be/K5xH4T_qcec">Cycles 3.1 Point Cloud Render</a>
  3. <a href="https://youtu.be/6iqVv8Xii-w">World Blender Meetup Day 2022 Presentation</a>
  
 

# Blog and Ephemera
  <a href="https://theplyguy.blogspot.com/">ThePLYGuy Blog</a>
  
  <a href="https://www.youtube.com/channel/UCO5O6Rh7vPvReCxiSGrU-FQ">Our YouTube Channel</a>
  
  <a href="https://blenderartists.org/t/blender-use-at-the-university-of-rochester-advancing-python-ply/1477882">BlenderArtists Article 8-13-2023</a>
