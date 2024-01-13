import numpy as np
from scipy.sparse import lil_matrix


def generate_weight_matrix(m, b, d_diff_thresh, pair_dist_thresh):
    assert m.shape[1] == b.shape[1]
    n = m.shape[1]
    w = -1.0e4 * np.ones((n * n, n * n))
    n_accepted_pairs = 0
    for p in range(n):
        for q in range(n):
            for s in range(n):
                for t in range(n):
                    if p == s or q == t:
                        continue
                    i = p + (q - 1) * n
                    j = s + (t - 1) * n
                    ps_dist = np.linalg.norm(m[:, p] - m[:, s])
                    qt_dist = np.linalg.norm(b[:, q] - b[:, t])
                    d_diff = abs(ps_dist - qt_dist)
                    if d_diff <= d_diff_thresh and ps_dist >= pair_dist_thresh and qt_dist >= pair_dist_thresh:
                        w[i, j] = np.exp(-d_diff)
                        n_accepted_pairs += 1
    return w, n_accepted_pairs


def generate_sdp_constraint_map(n, k):
    nn_1 = n * n + 1
    maps = [None] * (2 * n)

    for i in range(n):
        a = np.zeros((n, n))
        a[i, :] = 1
        av = np.hstack((a.flatten(), [0]))
        m = lil_matrix((nn_1, nn_1))
        for j in range(nn_1):
            m[nn_1 - 1, j] = av[j]
        maps[i] = m.tocsr()

    for i in range(n):
        a = np.zeros((n, n))
        a[:, i] = 1
        av = np.hstack((a.flatten(), [0]))
        m = lil_matrix((nn_1, nn_1))
        for j in range(nn_1):
            m[nn_1 - 1, j] = av[j]
        maps[n + i] = m.tocsr()

    maps_b = np.ones((2 * n, 1))
    m = lil_matrix((nn_1, nn_1))
    for j in range(nn_1):
        m[nn_1 - 1, j] = 1.0

    return maps, m.tocsr(), maps_b, k
