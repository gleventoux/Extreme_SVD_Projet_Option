import numpy as np
from scipy.linalg import svd
import primme
import time
import gc

@profile
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


@profile
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


@profile
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


print("Initialisation")

ligne = int(10**3)
colonne = int(10**3)
a_matrix = np.arange(0,ligne*colonne,step=1).reshape(ligne,colonne)
print(a_matrix)
nrb_max_sval=min(a_matrix.shape)

test_primme(a_matrix,6)
gc.collect()
test_numpy(a_matrix)
gc.collect()
test_scipy(a_matrix)


# if __name__== '__main__':
