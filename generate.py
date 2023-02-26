import os
import h5py
import numpy as np
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

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

    
        
            



        
    