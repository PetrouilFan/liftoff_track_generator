import numpy as np
import pyvista as pv
from pyvista import examples
from tkinter import filedialog
import liftofftrack as lot

PLOT = True
# TODO: Check if the density is correct and it works
DENSITY = 1 # in cubes per half meter
MAX_SIZE = 300 # in meters
ONLY_SURFACE = True

localId = "226a6ef8-11ac-42cb-b186-6755d6d1e654"
track = lot.Track("TestTrack", "1.6.3", localId)

stl_file = filedialog.askopenfilename(title="Select a File", filetypes=[("STL files", "*.stl"), ("All files", "*.*")])

surface = pv.read(stl_file)

voxels = pv.voxelize(surface, density=surface.length / MAX_SIZE*2, check_surface=False)
if PLOT:
    voxels.plot(opacity=1.00)

surface_voxels = voxels.extract_surface()

if ONLY_SURFACE:
    points = surface_voxels.points
else:
    points = voxels.points

spawn_point = [0,0,0]
min_x = np.min(points[:, 0])
min_y = np.min(points[:, 1])
spawn_point[0] = min_x - 10
spawn_point[2] = min_y - 10
sp = lot.SpawnPoint(len(track.objects), spawn_point, (0, 0, 0))
track.objects.append(sp)

# Cycle through every voxel
for i in range(points.shape[0]):
    point = points[i]
    # devide by 2 since the cube is 0.5m
    point = [point[0]/(DENSITY*2), point[1]/(DENSITY*2), point[2]/(DENSITY*2)]
    # swap y and z since the axis are different
    point = [point[0], point[2], point[1]]
    cube = lot.Cube05x05(len(track.objects), point, (0, 0, 0))
    track.objects.append(cube)

print(f"Total number of cubes: {len(track.objects)}")

track.export_file("output.track")
track.export_file(f"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Liftoff\\Liftoff_Data\\Tracks\\{localId}\\{localId}_0001.track")
