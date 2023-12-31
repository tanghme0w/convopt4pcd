from scipy.io import savemat
import numpy as np
import open3d as o3d

project = "temple"
instance = 1

data = np.asarray(o3d.io.read_point_cloud(f"data/{project}-pcd/{project}-pcd-{instance}.ply").points)
data = np.transpose(data)
mat_dict = {'array': data}
print(data.shape)
savemat(f'data/mat/{project}-{instance}.mat', mat_dict)
