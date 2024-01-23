import utils
import numpy as np

maps, mapeq, maps_b, mapeq_b = utils.generate_sdp_constraint_map(2, 2)
Y = np.asarray([[0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0]])
z = np.dot(mapeq, Y)
print(z)