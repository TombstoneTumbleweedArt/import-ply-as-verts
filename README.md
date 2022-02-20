# import-ply-as-verts
## Blender 3.1 Alpha (and later) PLY Importer
<ul>
  <li>Complete drop-in replacement for the stock Blender PLY import module.</li>
  <li>Correctly loads vertex-colored point clouds and nonstandard PLY files that the original importer wasn't meant for.</li>
  <li>Retains the functionality of the original codebase.</li>
</ul>

<strong>Experimental Branch:-</strong>   Final Beta commit, now testing ahead of 2.0 Release :)


# Why:

- Attempting to import any of the below PLY files with the stock importer will fail:
  
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

# Result:


<i>(Left to Right)</i>
  - Blender Export, Mesh and Cloud;  BTracer2, Mesh and Cloud;  J-Wildfire Cloud; Photogrammetry Cloud

There is only _one_ Material in this scene.

![The_Gang](https://user-images.githubusercontent.com/24717972/154849262-121f25f7-241f-4c16-b1e3-2b3ea0c77e65.jpg)

![The_Gang-Render](https://user-images.githubusercontent.com/24717972/154849235-78dd499c-ae07-4720-bf33-9a226f0cdac2.jpg)

The point cloud files have had a simple geometry node tree applied (included in the <i>example_x.blend</i> files)
