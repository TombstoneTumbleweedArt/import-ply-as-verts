# import-ply-as-verts v2.1 &nbsp; &nbsp; &nbsp; &nbsp; [![Generic badge](https://img.shields.io/badge/Release-2.1-<COLOR>.svg)](https://shields.io/) &nbsp; &nbsp; &nbsp; &nbsp; ![Logo_Blender-Dark](https://user-images.githubusercontent.com/24717972/154959144-bd55fdc0-2ab9-43e4-8747-33c7465a9c8f.svg)    
## Blender 3.0 * / 3.1 Alpha (and later) New PLY Importer

# NOTE: As of Blender 4.0 the original Python PLY import/export will be removed in favor of the new C++ modules.
        However, this repo will remain. :)
<ul>
  <li> * Vertex colored mesh only in 3.0 (see <strong>Compatibility</strong>).
  <li>Complete drop-in replacement for the stock Blender PLY import module.</li>
  <li>Correctly loads vertex-colored point clouds and nonstandard PLY files that the original importer wasn't intended for.</li>
  <li>Retains the functionality of the original codebase.</li>
</ul>

<strong>3 April 2022 - Version 2.1 Release</strong>: fixed several compatibility issues with various odd types of Ply.


 
# Why

- Attempting to import <i><strong>any</strong></i> of the below PLY files with the stock importer will fail:
  
   - Triangle/Quad Meshes with nonstandard file terminators <i>(BTracer2 PLY export)</i>
   
   - Zero edge/face point cloud files, ie:
    
     - Mandelbulb3D BTracer Point Cloud <i>(v.1.99 and earlier)</i>
     - Mandelbulb3D BTracer2 PLY <i>(1.99.12 and later)</i>
     - J-Wildfire Point Cloud    <i>(Some incompatible edge cases may yet exist.  They will be patched as needed.</i>
     - Photogrammetry scans  <i>(MeshLab,</i> et. al.<i>)</i>


 The result in Blender is the system console window error message "Invalid header, etc..."    



   ![Error-Message](https://user-images.githubusercontent.com/24717972/154848070-c59145aa-8d9e-4000-8de8-077cd3ad11f1.jpg)


Which has proven _most_ frustrating for several years now.

> Prior to this, a good workaround was to process the point cloud in MeshLab.  I love MeshLab and use it often, but it is daunting at best.  The <i>real</i> idea was to have native Blender import.
> Recent functions added under the hood of the Realize Instances node suddenly dovetailed with a standalone instancing app I had been working on since 2017.  Realizing that six nodes can replace my entire program, I cheerfully abandoned it and put full effort into the importer.

The combined result is a completely new workflow for the point cloud enthusiast.

# Result


> <i>(Left to Right, Back Row First)</i>
>   - <strong>Vertex-Painted Suzanne</strong> <i>(Same file as Mesh and Verts)</i>; 
>   - <strong>BTracer2</strong> <i>(Same file as Mesh and Verts)</i>;  
>   - <strong>J-Wildfire Point Cloud</strong>; 
>   - <strong>Photogrammetry Point Cloud</strong>

![The_Gang](https://user-images.githubusercontent.com/24717972/154947983-be7a2e52-a9f8-4114-b887-8933970f96c7.jpg)

![The_Gang-Render](https://user-images.githubusercontent.com/24717972/154948015-238c3d0d-43e4-4b63-a316-4f4470ce172d.jpg)

All the objects in this scene share a single Material of correctly imported vertex colors. The point clouds have a simple Geometry Node tree applied . <i>(Material and Nodetree included in the </i>Example.blend<i> file).</i>

# Cycles Point Cloud Render
The brand new Point Cloud Render mode in Cycles works beautifully well with these (thank you to <strong>Bone Studio</strong> and <strong>Daniel Leike</strong>).  A tutorial is available on <a href="https://www.youtube.com/watch?v=K5xH4T_qcec&t=1s">YouTube</a>, and our image was included in the <a href="https://wiki.blender.org/wiki/Reference/Release_Notes/3.1/Cycles">Blender 3.1 Release Notes - Cycles</a>

![31-Notes](https://user-images.githubusercontent.com/24717972/158804408-633a6bcf-fe94-416a-8e21-751b29687b2f.png)

# Compatibility

  - Mesh Import is verified for 3.0 (thanks to <strong>Carisma Alex</strong> for asking!) and works exactly like the process in <a href="https://youtu.be/4u-kS9IeTc4">Mandelbulb3D - BTracer2 Workflow Basic</a>.  However, the Point Cloud object requires new functionality added in Blender 3.1 to correctly assign the colors.  Direct import results in a charcoal briquette with missing surface normals.  A workaround is to create the Point Cloud in 3.1 (with applied Geo Node Modifier), save as a .blend file or export to a modern format like .gltf, and open in 3.0.  A call to (Edit Mode) Mesh->Normals->Recalculate Outside is usually necessary.


       ![Compatibility-sm](https://user-images.githubusercontent.com/24717972/155842926-f474fc6e-603a-4fa0-a1de-553f35df85ca.jpg)
         



# Install

  Since these are Scripts and not an Addon, the `__init__.py` and `import_ply.py` files from the repo will need to be manually pasted alongside the stock importer files.
  
  1. Open Blender's location on your computer.  On Windows this is generally <i>'C:\Program Files\Blender Foundation\'</i>
  2. If multiple version numbers are present, open the folder of the version you want to upgrade (for our example here, <i>'Blender 3.1'</i>)
  3. Open the <i>'3.1'</i> folder 
  4. Open the <i>'scripts'</i> folder
  5. Open the <i>'addons'</i> folder
  6. Open the <i>'io_mesh_ply'</i> folder
  7. Rename `'__init__.py'` to something like `'__init__-OLD.py'`
  8. Remame `'import_ply.py'` to something like `'import_ply-OLD.py'`
  9. Paste in the new `__init__.py` and `import_ply.py` from the repository
  10. Restart Blender
   
 <strong>This will need to be done once for each version of Blender you would like to use the script with</strong>. If you want to revert to the original script, reverse steps 7 and 8.
    
 The install procedure is also contained in `Install-v2.pdf` and <a href='https://youtu.be/UvC1IPhKNZU'>How to Install v2.0</a>.   

# Usage

Once the scripts are replaced, <i>File->Import</i> will now look like this:


![File_Screenshot](https://user-images.githubusercontent.com/24717972/154866087-3e15bcbc-8537-444c-af1d-4d41c4f25a36.jpg)

  
  Selecting <i>Stanford PLY as Verts</i> will bring up the Filebrowser as usual, with an additional checkbox:
  

![File-04-Screenshot](https://user-images.githubusercontent.com/24717972/155117073-40b5fb08-35a9-4ca9-8b42-32438515e98c.jpg)

Several things may happen at this point:
  - A triangle/quad mesh file may be loaded as either point cloud (checkbox selected) or mesh (checkbox deselected).
  - A point cloud file may be loaded with the checkbox selected.
  - A point cloud file may be loaded with the checkbox deselected, and the autodetect routine will use the correct loading method.
    - <i>Known Issue:- a bug in the autodetect slows performance as it causes the file to be read twice.  Currently working on a fix.</i>


# Performance
Importing a mesh is the heaviest operation, as importing the same file as verts is about 60% faster.  This is due to the triangle-building algorithm from the stock importer.  Improvements can be made here!

![Chart-03-SM](https://user-images.githubusercontent.com/24717972/163175009-83fa5c80-f3d1-4889-be28-c7af03cc61f7.jpg)

*Stock time is listed only for reference - it's faster because it bails out and produces an unusable model.

# Known Issues

   - The autodetect bug mentioned above.
   - The checkbox occasionally remains checked despite being False under the hood.  This is under investigation. 
   


# Python API
  
  The API call has a new optional Boolean parameter, `use_verts` (default=False):
  
   `bpy.ops.import_mesh.ply(filepath="", files=[], use_verts=False, directory="", filter_glob="*.ply")`
   
  and is used similar to
      
   `Dave = bpy.ops.import_mesh.ply(filepath="C:\\mb3d_mesh.ply", use_verts=True)`  
   
   <strong>Backward Compatibility</strong>
   
   A call like 
    ` Dave = bpy.ops.import_mesh.ply(filepath="C:\\mb3d_mesh.ply")` 
   is equivalent to using the stock importer and <i>shouldn't</i> break existing scripts.
    
    
    
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
  
  1. <a href='https://youtu.be/UvC1IPhKNZU'>How to Install v2.0</a>
  2. <a href="https://youtu.be/4u-kS9IeTc4">Mandelbulb3D - BTracer2 Workflow Basic</a>
  3. <i>Mandelbulb3D - BTracer2 Workflow Advanced</i>
  4. <i>J-Wildfire</i>
  5. <i>Photogrammetry Rescue with MeshLab and VisualSFM</i>
  6. <a href="https://youtu.be/K5xH4T_qcec">Cycles 3.1 Point Cloud Render</a>
  7. <a href="https://youtu.be/6iqVv8Xii-w">World Blender Meetup Day 2022 Presentation</a>
  8. <i>...</i>
 

# Blog and References
  <i>Under construction</i>
