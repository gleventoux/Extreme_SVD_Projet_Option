import os
import h5py
from sklearn.decomposition import IncrementalPCA
import dask.array as da


# TEST FUNCTIONS DEFINITION

@profile
def test_sklearn_ipca(filename):

    '''
    Parameters
    ----------
    filename : str
               Name of the .hdf5 file storing the matrix with the extension
    '''

    file_path = os.path.join("matrix",filename)

    with h5py.File(file_path,"r") as f:

        ipca = IncrementalPCA()

        for batch in f.keys():
            ipca.partial_fit(f[batch])

@profile
def test_dask_svd(filename):

    '''
    Parameters
    ----------
    filename : str
               Name of the .hdf5 file storing the matrix with the extension

    '''

    file_path = os.path.join("matrix",filename)
    
    with h5py.File(file_path,"r") as f:

        data = []

        for batch in f.keys():

            batch_shape = f[batch].shape
            data.append(da.from_array(f[batch],chunks=batch_shape))

    x = da.concatenate(data,axis=0)

    u, s, v = da.linalg.svd(x)


# TEST FUNCTIONS CALL

filename_list = os.listdir("matrix")
filename_list.remove(".gitkeep")

for filename in filename_list:

    test_sklearn_ipca(filename)
    test_dask_svd(filename)


