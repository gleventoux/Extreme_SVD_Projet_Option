import os
import numpy as np
import matplotlib.pyplot as plt
import h5py
import argparse

# splite a matrix from a .h5 file into nb iterations .h5 file
__file__ = "<path_to_file>"
CWD = os.getcwd()
CF  = os.path.realpath(__file__)
CFD = os.path.dirname(CF)
Matrix=os.path.join(CFD,"matrix")  
 
def data_splitter(filename,tar_dir,niters,nb_cols):

    f=h5py.File(os.path.join(Matrix,filename), 'r')
    
    num_datasets = len(f.keys())
    for i,datasetname in enumerate(f.keys()):
        if not i:
            dataset = f[datasetname]
            data_init=dataset[:,:].reshape(dataset.shape[0],-1)
        else:
            dataset = f[datasetname]
            data=dataset[:,:].reshape(dataset.shape[0],-1)
            data_init=np.vstack((data_init,data))        
        print(f"loading dataset {i}")
    print("loaded successfully !")
    
    filename_list=list()
    batch_size = int(nb_cols / niters)
    for iteration in range(niters):
        batch_data = data_init[:,iteration*batch_size:(iteration+1)*batch_size]
        h5f = h5py.File(os.path.join(tar_dir,f'splitted_{filename}_'+str(iteration)+'.hdf5'), 'w')
        h5f.create_dataset('dataset', data=batch_data)
        print(f"splitting data {iteration}")
        filename_list.append(os.path.join(tar_dir,f'splitted_{filename}_'+str(iteration)+'.hdf5'))
        h5f.close()
        
    print("splitted successfully !")
    return filename_list

# for test
# generate random matrix and save it into several .h5 files

# Function that generates a part of the matrix and saves it to a file
def generate_matrix_part(n, m, i):
    # Generate a random matrix using NumPy's random number generator functions
    matrix = np.random.random((n, m))
    print(matrix.shape)
    # Save the matrix to a file called "matrix_part_i.h5"
    with h5py.File(f"./matrix/randommatrix_part_{i}.h5", "w") as f:
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

# for checking

def print_structure_matrix(filenames):
    for filename in filenames:
        with h5py.File(filename, 'r') as f:
            root_keys = list(f.keys())
            for key in root_keys:
                print(f[key].shape)
        f.close()
        
if __name__ =="__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("filename",type=str,help='filename of the matrix required to split')
    # parser.add_argument("tar_dir",type=str,help='directory where you want to save these splitted matrice')
    # parser.add_argument("niters",type=int,help='number of iteration in streaming')
    # parser.add_argument("ncols",type=int,help='number of columns in the original matrix')
    
    #args = parser.parse_args()
    #filenames=data_splitter(args.filename,args.tar_dir,args.niters,args.ncols)
    print(Matrix)
    filenames=data_splitter('random1Go.hdf5',Matrix,5,5000)
    print_structure_matrix(filenames)
    #generate_matrix_files(100000,200,5)