import numpy as np
from scipy.linalg import svd
import primme
import dask.array as da
from sklearn.decomposition import IncrementalPCA
import h5py
import os


@profile
def test_numpy(filename):

    file_path = filename + ".hdf5"

    with h5py.File(file_path,"r") as f:

        batchs = []

        for key in f.keys():

            batchs.append(f[key][:])

        matrix = np.concatenate(batchs)
        u, s , vh = np.linalg.svd(matrix,full_matrices=False)

        print("Numpy")
        print( "S matrix shape ")
        print(s.shape)
        print(f"6 Largest Singular Values (includes machine 0):")
        print (s[:6])
        print("Left Singular vectors dimension")
        print(u.shape)
        print("Right Singular vectors dimension")
        print(vh.shape)

@profile
def test_scipy(filename):

    file_path = filename + ".hdf5"

    with h5py.File(file_path,"r") as f:

        batchs = []

        for key in f.keys():

            batchs.append(f[key][:])

        matrix = np.concatenate(batchs)
        u, s , vh = svd(matrix,full_matrices=False,overwrite_a=True, check_finite=False)
        
        print("Scipy svd")
        print( "S matrix shape ")
        print(s.shape)
        print(f"6 Largest Singular Values (includes machine 0):")
        print (s[:6])
        print("Left Singular vectors dimension")
        print(u.shape)
        print("Right Singular vectors dimension")
        print(vh.shape)

@profile
def test_primme(filename):

    file_path = filename + ".hdf5"

    with h5py.File(file_path,"r") as f:

        batchs = []

        for key in f.keys():

            batchs.append(f[key][:])

        matrix = np.concatenate(batchs)
        sv_number = np.min(matrix.shape)
        print( "Number of singular values to compute :")
        print(sv_number)
        
        svecs_left, svals, svecs_right = primme.svds(matrix,k = sv_number, tol=1e-9, which='LM')

        print("Test PRIMME")
        print(f" {sv_number} Largest Singular Values (includes machine 0):")
        print(svals)
        print("Left Singular vectors dimension")
        print(svecs_left.shape)
        print("Right Singular vectors dimension")
        print(svecs_right.shape)

@profile
def test_dask(filename):


    file_path = filename + ".hdf5"
    
    with h5py.File(file_path,"r") as f:

        data = []

        for batch in f.keys():

            batch_shape = f[batch].shape
            data.append(da.from_array(f[batch][:],chunks=batch_shape))

    x = da.concatenate(data,axis=0)

    u, s, vh = da.linalg.svd(x)

    print("Dask svd")
    print( "S matrix shape ")
    print(s.shape)
    print(f"6 Largest Singular Values (includes machine 0):")
    print(s.compute()[:6])
    print("Left Singular vectors dimension")
    print(u.shape)
    print("Right Singular vectors dimension")
    print(vh.shape)

@profile
def test_sklearn(filename):

    file_path = filename + ".hdf5"

    with h5py.File(file_path,"r") as f:

        ipca = IncrementalPCA()

        for batch in f.keys():
            ipca.partial_fit(f[batch][:])

    s = ipca.singular_values_

    print("SKL IPCA svd")
    print( "S matrix shape ")
    print(s.shape)
    print(f"6 Largest Singular Values (includes machine 0):")
    print (s[:6])
    print("Left Singular vectors dimension")
    #print(u.shape)
    print("Right Singular vectors dimension")
    #print(vh.shape)
 


# CALL

filename = "moyenne"

test_numpy(filename)
test_scipy(filename)
test_primme(filename)
test_dask(filename)
test_sklearn(filename)

    


