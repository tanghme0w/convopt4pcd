import copy
import json

import numpy as np
import open3d as o3d

# import info and read rotation
project = "bunny"
number = 2

with open(f"data/{project}-pcd/points.json") as pf:
    info = json.load(pf)
    rotation = info[f'pcd_{number}']['rotation']

pcd = o3d.io.read_point_cloud(f'data/{project}-pcd/{project}-pcd-1.ply')

pcd2 = o3d.io.read_point_cloud(f'data/{project}-pcd/{project}-pcd-{number}.ply')
pcd2_rotate = copy.deepcopy(pcd2)

pcd2_rotate.rotate(rotation, center=(0, 0, 0))
pcd2_rotate.translate(info[f'pcd_{number}']['translation'])

vis = o3d.visualization.Visualizer()
vis.create_window()

opt = vis.get_render_option()

vis.add_geometry(pcd)
vis.add_geometry(pcd2_rotate)
# vis.add_geometry(pcd2)

vis.run()
