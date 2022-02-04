# import-ply-as-verts
Blender 3.1 PLY importer that correctly loads point clouds (and all PLY models as point clouds)

The stock PLY importer that ships with Blender was never intended for vertex-colored point clouds (ie, PLY files with zero edges and faces). Most of my fun math graphics are point clouds from Mandelbulb3D, J-Wildfire, and photogrammetry scans gone horribly wrong. Until now, getting these clouds into Blender has involved a great deal of heavy lifting.
Since 2017 I have been developing a standalone app for this but with the recent functionality added in Blender 3.1 Alpha and newer, I happily abandon my project to throw full energy into the beauty of Geo Nodes.

Until I get the script correctly packaged as an addon, it will be necessary to replace the stock import module with the new one.  See the Install.pdf file for more detail.

![Node_Setup](https://user-images.githubusercontent.com/24717972/152527292-f0f03ad2-4cb2-4629-9b49-0ffea61bf968.jpg)
