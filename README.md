# import-ply-as-verts
<strong>Blender 3.1 Alpha (and later) PLY importer that correctly loads point clouds (and all PLY models as point clouds)</strong>

<b>Latest News</b>

* Mandelbulb3D - Recommended to use v1.99 for now.  The BTracer2 module in v1.99.32 isn't compatible with the importer yet but it's an easy patch, will be fixed asap.
* Feb 5, 2022 - v1.01 patched to allow for certain J-Wildfire formulas that add extraneous data to the PLY file during export.

Until I get the script correctly packaged as an addon, it will be necessary to replace the stock import module with the new one.  See the Install.pdf file for more detail.

The stock PLY importer that ships with Blender was never intended for vertex-colored point clouds (ie, PLY files with zero edges and faces). Most of my fun math graphics are point clouds from Mandelbulb3D, J-Wildfire, and photogrammetry scans gone horribly wrong. Until now, getting these clouds into Blender has involved a great deal of heavy lifting.
Since 2017 I have been developing a standalone app for this but with the recent functionality added in Blender 3.1 Alpha and newer, I happily abandon my project to throw full energy into the beauty of Geo Nodes.

I was able to sleuth out why the importer didn't work.  For the technically minded, the issue was that the Vertex Color Data Block in Blender is intimately tied to Faces.  One cannot exist without the other.  However, the color data was still being read in.  The tricky part was spending many quality hours with bpy.data. <autocomplete> to ultimately find a useful data structure for said color data.  Finally, a Custom Attribute was the answer!  
  
And now instead of endlessly coding ON point clouds, we all get to PLAY with point clouds. 

  
And hast thou slain the Jabberwock?
Come to my arms, my beamish boy!
O frabjous day! Callooh! Callay!
He chortled in his joy.

Lewis Carroll, 'The Jabberwocky'

  
  Demo Video: https://youtu.be/-OMV2LrTwVw


![Node_Setup-02](https://user-images.githubusercontent.com/24717972/152528698-3be48667-570c-4ab4-bbf7-75773cbd3582.jpg)
