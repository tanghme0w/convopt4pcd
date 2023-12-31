# import sys
#
# import numpy as np
# import open3d as o3d
#
# project = "bunny"
#
# for i in range(3):
#     # Load the PLY file
#     cloud_double = o3d.io.read_point_cloud(f"data/{project}-pcd/{project}-pcd-{i + 1}.ply")
#
#     # Convert to single precision
#     cloud_single = o3d.geometry.PointCloud()
#     cloud_single.points = o3d.utility.Vector3dVector(
#         [[float(p[0]), float(p[1]), float(p[2])] for p in cloud_double.points]
#     )
#
#     single_array = np.asarray(cloud_single.points)
#     size = sys.getsizeof(single_array[0, 0])
#
#     # Save the point cloud in single precision
#     o3d.io.write_point_cloud(f"data/{project}-pcd/{project}-pcd-{i + 1}_sp.ply", cloud_single, write_ascii=True, compressed=True)

def process_floats(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    processed_lines = []
    header_ended = False

    for line in lines:
        if header_ended:
            # Split the line into numbers, format them, and then join back
            numbers = line.split()
            formatted_numbers = ['{:.4f}'.format(float(num)) for num in numbers]
            processed_line = ' '.join(formatted_numbers) + '\n'
            processed_lines.append(processed_line)
        else:
            processed_lines.append(line)

        if line.strip() == "end_header":
            header_ended = True

    with open(output_file, 'w') as file:
        file.writelines(processed_lines)

project = "bunny"

for i in range(3):
    process_floats(f"data/{project}-pcd/{project}-pcd-{i + 1}.ply", f"data/{project}-pcd/{project}-pcd-{i + 1}_sp.ply")
