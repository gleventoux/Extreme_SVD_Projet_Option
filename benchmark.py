import os
import h5py
from sklearn.decomposition import IncrementalPCA


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
    print(file_path)

    with h5py.File(file_path,"r") as f:

        ipca = IncrementalPCA()

        for batch in f.keys():
            ipca.partial_fit(f[batch])


# TEST FUNCTIONS CALL

filename_list = os.listdir("matrix")
filename_list.remove(".gitkeep")

for filename in filename_list:

    test_sklearn_ipca(filename)


