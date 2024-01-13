import json
import open3d as o3d
import numpy as np


def load_data(project, instance):
    with open(f"data/{project}-pcd/points.json") as fp:
        info = json.load(fp)
        source_salient_idx = info[f'pcd_{instance}']['all_idxs']
        target_salient_idx = info['pcd_1']['all_idxs']

    # down sampling (use the salient points as the down sampled points)
    source = o3d.io.read_point_cloud(f'data/{project}-pcd/{project}-pcd-{instance}.ply')
    target = o3d.io.read_point_cloud(f'data/{project}-pcd/{project}-pcd-1.ply')
    source_down = o3d.geometry.PointCloud()
    source_down.points = o3d.utility.Vector3dVector(np.asarray(source.points)[source_salient_idx])
    target_down = o3d.geometry.PointCloud()
    target_down.points = o3d.utility.Vector3dVector(np.asarray(target.points)[target_salient_idx])

    return source, target, source_down, target_down
