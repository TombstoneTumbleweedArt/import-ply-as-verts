# import-ply-as-verts v3.0 &nbsp; &nbsp; &nbsp; &nbsp; [![Generic badge](https://img.shields.io/badge/Release-3.0-<COLOR>.svg)](https://shields.io/) &nbsp; &nbsp; &nbsp; &nbsp; ![Logo_Blender-Dark](https://user-images.githubusercontent.com/24717972/154959144-bd55fdc0-2ab9-43e4-8747-33c7465a9c8f.svg)    
## Blender Python PLY Import Addon

### Preamble
As of Blender 4.0 the original Python PLY import/export will be deprecated in favor of the new C++ modules.
These modules are a great deal faster (at the moment) but nowhere near as source-friendly as Python. 
Due to the flexible nature of the PLY format, compatibility with Blender has remained an issue. Our open-source
Python Addon is currently the most compatible and flexible option for nonstandard models such as point clouds.

### Thanks to Ms. Katherine Jarvis.

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

> *(Not actually trademarked, but innovative enough I feel she deserves one :).


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
 4. (Optional) Read the Manual.  <i>It's a good manual :)</i>
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
    
Once your model has loaded, a number of common use cases are included in the manual.


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
   
  > Load a PLY geometry file as verts or mesh
    
      Parameters: filepath (string, (optional, never None)) – File Path, Filepath used for importing the file
                  files (bpy_prop_collection of OperatorFileListElement, (optional)) – File Path, File path used for importing the PLY file
                  use_verts (boolean, (optional)) - Load as verts or triangle/quad mesh
                  hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings
                  directory (string, (optional, never None)) – directory
                  filter_glob (string, (optional, never None)) – filter_glob
  
  >   File: addons/io_mesh_ply/__init__.py:81


# Roadmap

   - Performance can likely be improved.  I haven't looked too deeply into the read() module which is a common bottleneck in file i/o.
   - Exporting Blender objects as verts is not yet supported.  Not a huge priority but will be addressed.
   - Various refactoring.
    
# Tutorials
  
## Note: These are a bit dated but essentially the same.  Newer videos are in the works.
  1. <a href="https://youtu.be/4u-kS9IeTc4">Mandelbulb3D - BTracer2 Workflow Basic</a>
  2. <a href="https://youtu.be/K5xH4T_qcec">Cycles 3.1 Point Cloud Render</a>
  3. <a href="https://youtu.be/6iqVv8Xii-w">World Blender Meetup Day 2022 Presentation</a>
  
 

# Blog and Ephemera
  <a href="https://theplyguy.blogspot.com/">ThePLYGuy</a>
