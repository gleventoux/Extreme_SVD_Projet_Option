import os
import h5py
import numpy as np

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

        last_batch_number,last_batch_size = divmod(n,batch_size)

        with h5py.File(file_path,'w') as file:
            
            for i in range(last_batch_number):
                batch = file.create_dataset("batch{}".format(i), shape=(batch_size,m))
                batch[:] = np.random.uniform(low,high,size=(batch_size,m))

            if last_batch_size != 0:
                batch = file.create_dataset("batch{}".format(last_batch_number), shape=(last_batch_size,m))
                batch[:] = np.random.uniform(low,high,size=(last_batch_size,m))

    else:
        print("Filename already used, matrix not generated.")

        
            



        
    