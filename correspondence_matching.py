import numpy
import numpy as np
import open3d as o3d
import cvxpy as cp

# for testing purpose only
project = "bunny"
instance = 1
o3d.io.read_point_cloud(f"data/{project}-pcd/{project}-pcd-{instance}.ply")


def correspondence_matching(
        source: o3d.geometry.PointCloud,
        target: o3d.geometry.PointCloud,
        source_feature: np.ndarray,
        target_feature: np.ndarray):

    N = min(source.points.size(), target.points.size())
    # initialize matching matrix
    A = numpy.ndarray(shape=(N**2, N**2))
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    pass

    # defining the SDP problem
    # the target matrix
    X = numpy.ndarray(shape=(N, N))

