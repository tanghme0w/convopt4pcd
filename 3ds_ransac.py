import copy
import numpy as np
import open3d as o3d
import open3d.cpu.pybind.pipelines.registration
from tqdm import tqdm
import json

import read_pcd

# config
project = "room"
instance = 3

dim = 128
r = "1.500000"
n = "16"
h = "1.750000"
trials = 100

voxel_size = 1.5

source_color = np.asarray([1, 0, 0])
transformed_source_color = np.asarray([0, 1, 0])
target_color = np.asarray([0, 0, 1])

source, target, source_down, target_down = pcdio.load_data(project, instance)

source_feature = open3d.pipelines.registration.Feature()
source_data = np.load(f"data/3ds-feature/{dim}dim/{project}-pcd-{instance}.ply_{r}_{n}_{h}_3DSmoothNet.npz")['data']#[source_salient_idx]
source_feature.data = source_data

target_feature = open3d.pipelines.registration.Feature()
target_data = np.load(f"data/3ds-feature/{dim}dim/{project}-pcd-1.ply_{r}_{n}_{h}_3DSmoothNet.npz")['data']#[target_salient_idx]
target_feature.data = target_data

def execute_global_registration(source_down, target_down, source_feature,
                                target_feature, voxel_size):
    distance_threshold = voxel_size * 1.5
    # print(":: RANSAC registration on downsampled point clouds.")
    # print("   Since the downsampling voxel size is %.3f," % voxel_size)
    # print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_feature, target_feature, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result


result_ransac = execute_global_registration(source_down, target_down,
                                            source_feature, target_feature,
                                            voxel_size)

for i in tqdm(range(trials)):
    temp_result_ransac = execute_global_registration(source_down, target_down,
                                                     source_feature, target_feature,
                                                     voxel_size)
    if temp_result_ransac.inlier_rmse < result_ransac.inlier_rmse:
        result_ransac = temp_result_ransac


transformation = result_ransac.transformation
print(result_ransac.inlier_rmse)

transformed_source = copy.deepcopy(source)
transformed_source.transform(transformation)

# output to file
o3d.io.write_point_cloud(f"data/ransac/{project}{instance}.ply", transformed_source, write_ascii=True)

# set color
transformed_source.paint_uniform_color(transformed_source_color)
source.paint_uniform_color(source_color)
target.paint_uniform_color(target_color)

vis = o3d.visualization.Visualizer()
vis.create_window('3ds_ransac')

# vis.add_geometry(source)
vis.add_geometry(target)
vis.add_geometry(transformed_source)

render_opt = vis.get_render_option()
render_opt.point_size = 4.0
vis.run()
