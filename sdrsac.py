import read_pcd
import sdp
import numpy as np

# for testing purpose only
project = "bunny"
instance = 1

source, target, source_salient, target_salient = pcdio.load_data(project, instance)

max_itr = 10000
n_sample = 5
k = 4
d_diff_thresh = 1.0e-4
pair_dist_thresh = 1.0e-2
n_pair_thres = 5
corr_count_eps = 0.015
icp_thres = 0.02


source_salient = np.asarray(source_salient.points)
target_salient = np.asarray(target_salient.points)

# random sample
idx_sample = np.random.choice(source_salient.shape[0], n_sample, False)
source_sample = source_salient[idx_sample, :]
target_sample = target_salient[idx_sample, :]

rot, t, corr_m, corr_b = sdp.sdp_reg(source_sample.T, target_sample.T,
                                     k, d_diff_thresh,
                                     pair_dist_thresh,
                                     n_pair_thres)


print(rot, t, corr_m, corr_b)
