import os
import h5py
import numpy as np
from scipy.stats import ortho_group
import math as mt
import argparse


def generate_random(filename,n,m,low=0,high=1,batch_size=1000):
    """
    # TODO : Brief description of the function

    Parameters
    ----------
    filename : str
               Name of the .hdf5 file which will store the matrix (without extension)
    n : int
        Number of rows
    m : int
        Number of columns
    low : float, optional
          Lower bound of the matrix entries
    high : float, optional
           Upper bound of the matrix entries
    batch_size : int, optional
                 # TODO : description of batch_size
          
    """
    
    file_path = os.path.join("matrix",filename) + ".hdf5"
    
    if not os.path.exists(file_path):

        if high < low:
            low,high = 0, 0

        full_batch_number, leftover_batch_size = divmod(n,batch_size)
        batch_number = full_batch_number + int(leftover_batch_size != 0)
        batch_label = "batch{:0" + str(len(str(batch_number-1))) + "}" 
        

        with h5py.File(file_path,'w') as file:
            
            for i in range(full_batch_number):
                batch = file.create_dataset(batch_label.format(i), shape=(batch_size,m),dtype='float64')
                batch[:] = np.random.uniform(low,high,size=(batch_size,m))

            if leftover_batch_size != 0:
                batch = file.create_dataset(batch_label.format(batch_number-1), shape=(leftover_batch_size,m),dtype='float64')
                batch[:] = np.random.uniform(low,high,size=(leftover_batch_size,m))

    else:
        print("Filename already used, matrix not generated.")


def generate_svd_known(n,m,filename="MatrixTest",low=0,high=100,bsize=10):
    """
    Generate random matrix and save its SVD.

    Parameters:
    ===========
    n : int
        Number of rows
    m : int
        Number of columns
    filename : str, optional
            Name of the .hdf5 file which will store the matrix (without extension)
    low : float, optional
          Lower bound for singular values
    high : float, optional
           Upper bound for singular values
    bsize : int, optional

    """

    S = np.zeros((n,m)) # n x m 
    U = ortho_group.rvs(n) # n x n 
    V = ortho_group.rvs(m) # m x m 

    singular_values = np.random.uniform(low,high,m) # min(n,m) = m singular values
    singular_values.sort()

    D = np.diag(singular_values[::-1])
    S[:m,:] = D

    M = U @ S @ V.T # n x m, test matrix

    # Matrix and SVD saves

    matrix_path = os.path.join("matrix",filename) + ".hdf5"
    svd_path = os.path.join("matrix",filename + "SVD") + ".hdf5"

    if not os.path.exists(matrix_path) and not os.path.exists(svd_path):

        with h5py.File(svd_path,'w') as file:
            
            file.create_dataset("U", shape=(n,n),data=U,dtype='float64')
            file.create_dataset("S", shape=(n,m),data=S,dtype='float64')
            file.create_dataset("V", shape=(m,m),data=V,dtype='float64')
            file.create_dataset("M", shape=(n,m),data=M,dtype='float64')

        with h5py.File(matrix_path,'w') as file:

            full_batch_number, leftover_batch_size = divmod(n,bsize)
            batch_number = full_batch_number + int(leftover_batch_size != 0)
            batch_label = "batch{:0" + str(len(str(batch_number-1))) + "}"

            for i in range(full_batch_number):

                file.create_dataset(batch_label.format(i), shape=(bsize,m),data=M[i*bsize:(i+1)*bsize,:],dtype='float64')
            
            if leftover_batch_size != 0:
                
                file.create_dataset(batch_label.format(batch_number-1), shape=(leftover_batch_size,m),data=M[full_batch_number*bsize:,:],dtype='float64')


def generate_random_wrapper(args):
    """
    Wrapper of the generate_random function called 
    when cli user chose matrix type = random

    Parameters
    ==========
    args : argparse.Namespace
        Struct whose attributs are the parameters of the generate_random function 

    """

    generate_random(args.filename,args.n,args.m,args.low,args.high,args.bsize)

def generate_svd_known_wrapper(args):
    """
    Wrapper of the generate_svd_known function called 
    when cli user chose matrix type = svd_known

    Parameters
    ==========
    args : argparse.Namespace
        Struct whose attributs are the parameters of the generate_svd_known function 

    """

    generate_svd_known(args.n,args.m,args.filename,args.low,args.high,args.bsize)




def main():

    parser = argparse.ArgumentParser(description="Generate matrix to test SVD methods")

    # We define subparsers for all type of matrix.
    subparsers = parser.add_subparsers(description="Choose matrix type.")

    # Definition for random matrix
    parser_random = subparsers.add_parser("random",description="Generate random matrix")

    parser_random.add_argument("filename",type=str, help="filename without extension")
    parser_random.add_argument("n",type=int,help="number of rows")
    parser_random.add_argument("m",type=int,help="number of columns")
    parser_random.add_argument("--low",type=float,required=False,default=0,help="lower bound for matrix entries")
    parser_random.add_argument("--high",type=float,required=False,default=1,help="upper bound for matrix entries")
    parser_random.add_argument("--bsize",type=int,required=False,default=1000,help="batch number of rows")

    parser_random.set_defaults(func=generate_random_wrapper)

    # Definition for svd-known matrix
    parser_svd_known = subparsers.add_parser("svd_known",description="Generate random matrix with its SVD")

    parser_svd_known.add_argument("n",type=int,help="number of rows")
    parser_svd_known.add_argument("m",type=int,help="number of columns")
    parser_svd_known.add_argument("--filename",type=str,required=False,default="MatrixTest", help="filename without extension")
    parser_svd_known.add_argument("--low",type=float,required=False,default=0,help="lower bound for singular values")
    parser_svd_known.add_argument("--high",type=float,required=False,default=100,help="upper bound for singular values")
    parser_svd_known.add_argument("--bsize",type=int,required=False,default=1000,help="batch number of rows")

    parser_svd_known.set_defaults(func=generate_svd_known_wrapper)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

    
        
            



        
    