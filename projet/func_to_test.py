import numpy as np
from scipy.linalg import svd
import primme
import time


def test_primme(matrix,sv_number):
    print("Test PRIMME")
    try :
        start = time.time()
        svecs_left, svals, svecs_right = primme.svds(matrix,k = sv_number, tol=1e-9, which='LM')
        print(f" Duration : {time.time() -start} seconds")
        print(f" {sv_number} Largest Singular Values (includes machine 0):")
        print(svals)
        print("Left Singular vectors dimension")
        print(svecs_left.shape)
        print("Right Singular vectors dimension")
        print(svecs_right.shape)
    except Exception:
        print(Exception)


def test_numpy(matrix):
    print("Numpy svd")
    try :
        start = time.time()
        u, s , vh = np.linalg.svd(matrix,full_matrices=False)
        print(f" Duration : {time.time() -start} seconds")
        print( "S matrix shape ")
        print(s.shape)
        print(f"6 Largest Singular Values (includes machine 0):")
        print (s[:6])
        print("Left Singular vectors dimension")
        print(u.shape)
        print("Right Singular vectors dimension")
        print(vh.shape)
    except Exception as error :
        print(error)


def test_scipy(matrix):
    print("Scipy svd")
    try :
        start = time.time()
        u, s , vh = svd(matrix,full_matrices=False,overwrite_a=True, check_finite=False)
        print(f" Duration : {time.time() -start} seconds")
        print( "S matrix shape ")
        print(s.shape)
        print(f"6 Largest Singular Values (includes machine 0):")
        print (s[:6])
        print("Left Singular vectors dimension")
        print(u.shape)
        print("Right Singular vectors dimension")
        print(vh.shape)
    except Exception as error :
        print(error)


