import numpy as np
from scipy.linalg import svd
import primme
import time
import gc
%load_ext line_profiler

print("Initialisation")

ligne = int(10**3)
colonne = int(10**3)
a_matrix = np.arange(0,ligne*colonne,step=1).reshape(ligne,colonne)
print(a_matrix)
nrb_max_sval=min(a_matrix.shape)


def test_primme():
    print("Test PRIMME")
    try :
        start = time.time()
        svecs_left, svals, svecs_right = primme.svds(a_matrix,k = 6, tol=1e-9, which='LM')
        print(f" Duration : {time.time() -start} seconds")
        print(svals)
        print(svecs_left.shape)
        print(svecs_right.shape)
    except Exception:
        print(Exception)


def test_numpy():
    print("Numpy svd")
    try :
        start = time.time()
        u, s , vh = np.linalg.svd(a_matrix,full_matrices=False)
        print(f" Duration : {time.time() -start} seconds")
        print(s.shape)
        print (s[:6])
        print(u.shape)
        print(vh.shape)
    except Exception as error :
        print(error)


def test_scipy():
    print("Scipy svd")
    try :
        start = time.time()
        u, s , vh = svd(a_matrix,full_matrices=False,overwrite_a=True, check_finite=False)
        print(f" Duration : {time.time() -start} seconds")
        print(s.shape)
        print (s[:6])
        print(u.shape)
        print(vh.shape)
    except Exception as error :
        print(error)


if __name__== '__main__':
    %lprun -f test_primme test_primme()
    gc.collect()
    %lprun -f test_numpy test_numpy()
    gc.collect()
    %lprun -f test_scipy test_scipy()
