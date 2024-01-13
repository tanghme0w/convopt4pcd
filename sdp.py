import cvxpy
import numpy as np
import picos
from cvxopt import matrix, spmatrix
from linear_projection import linear_projection
import utils
from kabsch import kabsch
import cvxpy as cp


def to_spmatrix(sp):
    coo = sp.astype(np.double).tocoo()
    return spmatrix(coo.data.tolist(), coo.row.tolist(), coo.col.tolist(), size=sp.shape)


def solve_sdp(w, k):
    nsquare = w.shape[0]
    n = int(np.sqrt(nsquare))
    ww = np.c_[w, np.zeros((nsquare, 1))]
    ww = np.r_[ww, np.zeros((1, nsquare + 1))]
    maps, mapeq, maps_b, mapeq_b = utils.generate_sdp_constraint_map(n, k)

    sdp = picos.Problem()
    y = sdp.add_variable('y', (nsquare + 1, nsquare + 1), 'symmetric')
    sdp.add_constraint(y >> 0)
    sdp.add_constraint(y[nsquare, nsquare] == 1.0)
    sdp.add_constraint(y[nsquare, :] == y[:, nsquare].T)
    for i, m in enumerate(maps):
        sdp.add_constraint(to_spmatrix(m) | y <= maps_b.astype(np.double)[i, 0])
    sdp.add_constraint(to_spmatrix(mapeq) | y == matrix(mapeq_b))
    sdp.add_constraint(picos.trace(y) == k + 1)
    sdp.set_objective('max', matrix(ww) | y)
    sdp.set_option('tol', 0.1)
    sdp.set_option('verbose', 0)
    # print(sdp)
    sdp.solve()

    y = y.value
    t = np.array(y[-1, :-1])
    x1 = t.reshape((n, n))
    x = linear_projection(x1.ravel(order='F'))

    idx, = np.where(x.ravel(order='F') == 1.0)
    score = x1.ravel(order='F')[idx]
    sidx = np.argsort(score)
    idx = np.delete(idx, sidx[(n - k):])
    x.ravel(order='F')[idx] = 0.0
    return x


def solve_sdp_cvx(w, k):
    nsquare = w.shape[0]
    n = int(np.sqrt(nsquare))
    ww = np.c_[w, np.zeros((nsquare, 1))]
    ww = np.r_[ww, np.zeros((1, nsquare + 1))]
    maps, mapeq, maps_b, mapeq_b = utils.generate_sdp_constraint_map(n, k)

    # Assuming genSDPConstraintMap generates constraint matrices and vectors
    # This function needs to be defined in Python or replaced with equivalent logic

    # Define the variable for the SDP
    Y = cp.Variable((nsquare + 1, nsquare + 1), symmetric=True)

    # Define the objective function
    objective = cp.Maximize(cp.trace(ww @ Y))

    # Define the constraints
    constraints = [
        Y >> 0,
        Y[nsquare, nsquare] == 1,
        Y[nsquare, :] == Y[:, nsquare],
        cp.trace(Y) == k + 1]

    for i, m in zip(maps, maps_b):
        constraints.append(i @ Y <= m)

    constraints.append(mapeq.data @ Y == mapeq_b)

    # Define and solve the problem
    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.CVXOPT, abstol=0.01, verbose=True)

    # Extract the solution
    Y_value = Y.value
    t = Y_value[-1, :-1]
    X1 = np.reshape(t, (n, n))

    # Assuming linearProjection is a function for post-processing
    # This function needs to be defined in Python or replaced with equivalent logic
    X = linear_projection(X1.flatten())

    # Further processing to extract k elements
    # This part of the code needs to be adapted according to the functionality of linearProjection
    idx = np.where(X == 1)[0]
    score = X1[idx]
    sidx = np.argsort(score)
    idx = np.delete(idx, sidx[n - k:])
    X[idx] = 0

    return X


def count_correspondence(m, tree, eps):
    dist, idx = tree.query(m.T)
    in_idx, = np.where(dist <= eps)
    return len(in_idx)


def get_correspondences(x):
    idxs = np.argmax(x, axis=1)
    y = x[np.arange(x.shape[0]), idxs]
    corr_m = np.where(y > 0)[0]
    corr_b = idxs[corr_m]
    return corr_m, corr_b


def sdp_reg(m, b, k, d_diff_thresh, pair_dist_thresh, n_pair_thres):
    w, n_accepted_pairs = utils.generate_weight_matrix(m, b,
                                                       d_diff_thresh,
                                                       pair_dist_thresh)
    if n_accepted_pairs <= n_pair_thres:
        return None, None, None, None

    # x = solve_sdp(w, k)
    x = solve_sdp_cvx(w, k)
    corr_m, corr_b = get_correspondences(x)
    sm = m[:, corr_m]
    sb = b[:, corr_b]
    rot, t = kabsch(sm, sb)
    return rot, t, corr_m, corr_b
