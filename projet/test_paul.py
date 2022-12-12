import numpy as np
from scipy.linalg import svd
import primme
import time

# sigma_matrix = np.diag([1,2,3])

# print(sigma_matrix.shape)
# v_matrix = np.array([[1, 1, 9, 3, 3, 7],
#        [5, 1, 7, 0, 3, 9],
#        [9, 8, 1, 1, 8, 9]])

# print(v_matrix.shape)
# u_matrix = np.array([[2, 8, 3],
#        [6, 9, 5],
#        [4, 0, 4],
#        [6, 1, 1],
#        [2, 3, 0],
#        [3, 4, 7]])

# print(u_matrix.shape)
# a_matrix = u_matrix @ sigma_matrix @ v_matrix


print("Initialisation")

ligne = int(10**3)
colonne = int(10**3)
a_matrix = np.arange(0,ligne*colonne,step=1).reshape(ligne,colonne)
print(a_matrix)
nrb_max_sval=min(a_matrix.shape)



@profile
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


@profile
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


@profile
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
    test_primme()
    test_numpy()
    test_scipy()
