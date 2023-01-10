import h5py
import numpy as np

# generate random matrix and save it into several .h5 files

# Function that generates a part of the matrix and saves it to a file
def generate_matrix_part(n, m, i):
    # Generate a random matrix using NumPy's random number generator functions
    matrix = np.random.random((n, m))
    print(matrix.shape)
    # Save the matrix to a file called "matrix_part_i.h5"
    with h5py.File(f"./data/data_generate/randommatrix_part_{i}.h5", "w") as f:
        # Create a dataset in the file with the same shape as the matrix
        dset = f.create_dataset("matrix", data=matrix)
    """
    One potential error is that the h5py library is not able to handle data of this size. 
    The size_i data type, which is used to represent the size of arrays in h5py, 
    has a maximum value of 2147483647. If the size of your data is larger than this, h5py will not be able to convert it to the size_i data type, 
    and   "can't convert from size to size_i" error.
    One potential solution is to try using a different data type to represent the size.
    For example, use the size_t data type
    """

# Generate nbatches parts of the matrix and save them to separate files
def generate_matrix_files(nlignes,ncols,nbatches):
    for i in range(nbatches):
        # for 8 GB memory each batch: nlignes = 10000000, ncols=100
        generate_matrix_part(nlignes, ncols, i)


if __name__ =="__main__":
    generate_matrix_files(100000,200,5)