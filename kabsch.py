import numpy as np


def kabsch(A, B):
    assert len(A) == len(B)

    N = A.shape[0]  # total points

    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)

    # center the points
    AA = A - centroid_A
    BB = B - centroid_B

    # dot is matrix multiplication for array
    H = np.dot(np.transpose(BB), AA)

    U, S, Vt = np.linalg.svd(H)

    R = np.dot(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) < 0:
        print("Reflection detected")
        Vt[2, :] *= -1
        R = np.dot(Vt.T, U.T)

    t = centroid_A - np.dot(R, centroid_B)

    return R, t


# Test the kabsch function
def test_kabsch():
    np.random.seed(0)  # For reproducibility

    # Create a random set of points
    A = np.random.rand(10, 3)

    # Create a rotation matrix
    theta = np.radians(45)  # 45 degree rotation
    c, s = np.cos(theta), np.sin(theta)
    R_true = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

    # Create a translation vector
    t_true = np.array([1, 2, 3])

    # Apply rotation and translation to create a second set of points
    B = np.dot(A, R_true.T) + t_true

    # Use the Kabsch algorithm to find R and t
    R, t = kabsch(A, B)

    # Apply R and t to A
    B_Aligned = np.dot(B, R.T) + t

    # Check if the aligned points are close to B
    return np.allclose(B_Aligned, A, atol=1e-6)


# Run the test
if test_kabsch():
    print("Test passed: Kabsch algorithm works correctly.")
else:
    print("Test failed: Kabsch algorithm has issues.")