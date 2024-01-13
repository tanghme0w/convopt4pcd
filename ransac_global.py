import copy
import numpy as np
import open3d as o3d
from tqdm import tqdm
import json

import read_pcd

# config
project = "room"
instance = 2
voxel_size = 1.5
source_color = np.asarray([1, 0, 0])
transformed_source_color = np.asarray([0, 1, 0])
target_color = np.asarray([0, 0, 1])


source, target, source_down, target_down = pcdio.load_data(project, instance)

source.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=3 * voxel_size, max_nn=30))
target.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=3 * voxel_size, max_nn=30))
source_fpfh = o3d.pipelines.registration.compute_fpfh_feature(source, o3d.geometry.KDTreeSearchParamHybrid(radius=5 * voxel_size, max_nn=100))
target_fpfh = o3d.pipelines.registration.compute_fpfh_feature(target, o3d.geometry.KDTreeSearchParamHybrid(radius=5 * voxel_size, max_nn=100))


def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    # print(":: RANSAC registration on downsampled point clouds.")
    # print("   Since the downsampling voxel size is %.3f," % voxel_size)
    # print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result


result_ransac = execute_global_registration(source, target,
                                            source_fpfh, target_fpfh,
                                            voxel_size)

# for i in tqdm(range(100)):
#     temp_result_ransac = execute_global_registration(source, target,
#                                             source_fpfh, target_fpfh,
#                                             voxel_size)
#     if temp_result_ransac.inlier_rmse < result_ransac.inlier_rmse:
#         result_ransac = temp_result_ransac

transformation = result_ransac.transformation
print(result_ransac.inlier_rmse)

transformed_source = copy.deepcopy(source)
transformed_source.transform(transformation)

# set color
transformed_source.paint_uniform_color(transformed_source_color)
source.paint_uniform_color(source_color)
target.paint_uniform_color(target_color)

vis = o3d.visualization.Visualizer()
vis.create_window('ransac')

# vis.add_geometry(source)
vis.add_geometry(transformed_source)
vis.add_geometry(target)

render_opt = vis.get_render_option()
render_opt.point_size = 4.0
vis.run()
