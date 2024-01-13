import numpy as np
from scipy.io import savemat
import json
import open3d as o3d

project = "bunny"
instance = 1

with open(f"data/{project}-pcd/points.json") as fp:
    info = json.load(fp)
    salient_idx = info[f'pcd_{instance}']['all_idxs']

# down sampling (use the salient points as the down sampled points)
data = o3d.io.read_point_cloud(f'data/{project}-pcd/{project}-pcd-{instance}.ply')
data = np.asarray(data.points)[salient_idx]
print(data.shape)
mat_dict = {f'salient_{project}{instance}': data.T}
savemat(f'data/mat/{project}-{instance}-salient.mat', mat_dict)