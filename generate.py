import os
import h5py
import numpy as np
import argparse


def generate(filename,n,m,low=0,high=1,batch_size=1000):

    '''

    # TODO : Brief description of the function

    Parameters
    ----------
    filename : str
               Name of the .hdf5 file which will store the matrix
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
          
    '''
    
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",type=str)
    parser.add_argument("n",type=int)
    parser.add_argument("m",type=int)
    parser.add_argument("--low",type=float,required=False,default=0)
    parser.add_argument("--high",type=float,required=False,default=1)
    parser.add_argument("--batch_size",type=int,required=False,default=1000)

    args = parser.parse_args()

    generate(args.filename,args.n,args.m,args.low,args.high,args.batch_size)
    
if __name__ == "__main__":
    main()



        
            



        
    