from scipy.io import savemat
import numpy as np
import json

projects = ['bunny', 'room', 'temple']
dim = 128
r = "1.500000"
n = "16"
h = "1.750000"
trials = 100

for project in projects:
    if project == "bunny":
        r = "0.150000"
    else:
        r = "1.500000"
    for instance in [1, 2, 3]:
        with open(f"data/{project}-pcd/points.json") as fp:
            info = json.load(fp)
            salient_idx = info[f'pcd_{instance}']['all_idxs']

        data = np.load(f"data/3ds-feature/{dim}dim/{project}-pcd-{instance}.ply_{r}_{n}_{h}_3DSmoothNet.npz")['data'][salient_idx]
        mat_dict = {f'feat_{project}{instance}': data}
        print(data.shape)
        savemat(f'data/mat_feat/{project}-{instance}-feature.mat', mat_dict)
