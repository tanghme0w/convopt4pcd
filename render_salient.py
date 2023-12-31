import numpy as np
import open3d as o3d
import json

project = "temple"
pcdList = []

for i in range(3):
    pcdList.append(o3d.io.read_point_cloud(f"data/{project}-pcd/{project}-pcd-{i + 1}.ply"))

with open(f"data/{project}-pcd/points.json") as fp:
    info = json.load(fp)
    print(info.keys())
    print(info['pcd_1']['uncertainty'])


default_color = np.asarray([[1, 1, 0], [0, 1, 0], [1, 0, 1]])
renderList = [1, 2]
print(default_color[1].shape)

for i in range(3):
    colors_array = np.zeros_like(pcdList[i].points)
    colors_array[:, :] = np.broadcast_to(default_color[i], colors_array.shape)
    saddle_idx = info[f'pcd_{i+1}']['all_idxs']
    for idx in saddle_idx:
        colors_array[idx] = [0, 0, 0]
    pcdList[i].colors = o3d.utility.Vector3dVector(colors_array)

vis = o3d.visualization.Visualizer()
vis.create_window()
for i in renderList:
    vis.add_geometry(pcdList[i - 1])

render_opt = vis.get_render_option()
render_opt.point_size = 4.0
vis.run()
