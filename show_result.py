import open3d as o3d
import numpy as np


project = "temple"
instance = 3
source_color = np.asarray([1, 0, 0])
transformed_source_color = np.asarray([0, 1, 0])
target_color = np.asarray([0, 0, 1])


source = o3d.io.read_point_cloud(f'data/{project}-pcd/{project}-pcd-{instance}.ply')
target = o3d.io.read_point_cloud(f'data/{project}-pcd/{project}-pcd-1.ply')
transformed_source = o3d.io.read_point_cloud(f'data/fonly/{project}{instance}-transform.ply')


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
