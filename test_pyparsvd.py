# Import the required libraries
import os
import sys
import time
import numpy as np
from mpi4py import MPI
import h5py
from netCDF4 import Dataset

# Define the __file__ global variable
__file__ = "<path_to_file>"
# Current, parent and file paths
CWD = os.getcwd()
CF  = os.path.realpath(__file__)
CFD = os.path.dirname(CF)

# Import library specific modules
sys.path.append(os.path.join("./"))
from pyparsvd.parsvd_serial   import ParSVD_Serial
from pyparsvd.parsvd_parallel import ParSVD_Parallel



# method for importing data from .h5 files into the forms suitable for parallel calculation
def load_h5_parallel(filename,comm,rank,nprocs,dataset):
    """
    This code loads a dataset from an HDF5 file and 
    returns a portion of the dataset based on the rank 
    and number of processes of the calling MPI process.

    Args:
        filename   : the path to the HDF5 file that contains the dataset
        comm   : the MPI communicator object that is used to communicate between the MPI processes.
        rank   : the rank of the calling MPI process
        nprocs   : the number of MPI processes that are running the code.
        dataset   : the name of the dataset in the HDF5 file that should be loaded

    Returns:
        a portion of the dataset
    """
    h5_file = h5py.File(filename, 'r', driver='mpio', comm=comm)
    dset = h5_file[dataset]
    ndof=dset.shape[0]
    # the number of rows that each MPI process should receive, 
    # based on the total number of rows and the number of processes. 
    num_rows_rank = int(ndof/nprocs)

    # If the rank of the calling MPI process is not the last process
    # the function returns a portion of the dataset that contains num_rows_rank rows, 
    # starting from the row index rank*num_rows_rank.
    # which may receive fewer rows if the total number of rows is not divisible by the number of processes.
    if rank != nprocs-1:
        rval =  dset[rank*num_rows_rank:(rank+1)*num_rows_rank,:].reshape(num_rows_rank,-1)
    else:
        num_dof_local = ndof - rank*num_rows_rank
        rval =  dset[rank*num_rows_rank:,:].reshape(num_dof_local,-1)
    h5_file.close()
    return rval

# method for importing data from .h5 files into the forms suitable for serial calculation
def load_h5_serial(filename,datasetname):
    """
    This code loads a dataset from an HDF5 file return a numpy array form data suitable for serial calculation
    
    Args:
        filename   : the path to the HDF5 file that contains the dataset
        datasetname : the name of the dataset in HDF5 file

    Returns:
        a portion of the dataset
    """    
    h5_file = h5py.File(filename, 'r')
    dataset = h5_file[datasetname]
    dataset=dataset[:,:].reshape(dataset.shape[0],-1)
    h5_file.close()
    return dataset

def load_nc_parallel(filename,comm,rank,nprocs,datasetname):
    """
    This code loads a dataset from an nc file return a numpy array form data suitable for parallel calculation
    
    Args:
        filename   : the path to the nc file that contains the dataset
        datasetname : the name of the dataset in HDF5 file

    Returns:
        a portion of the dataset
    """   
    nc_file = Dataset(filename,'r',format='NETCDF4',parallel=True)
    
    if rank != nprocs-1:
        
        num_rows_rank = int(nc_file[datasetname].shape[1]/nprocs)
        num_cols_rank = int(nc_file[datasetname].shape[2]/nprocs)
        
        rval =  nc_file[datasetname][:,:,
                                rank*num_cols_rank:(rank+1)*num_cols_rank
                                ].reshape(-1,nc_file[datasetname].shape[1]*num_cols_rank).T
        
    else:
        
        num_rows_rank = int(nc_file[datasetname].shape[1]/nprocs)
        num_rows_local = nc_file[datasetname].shape[1] - rank*num_rows_rank
        
        num_cols_rank = int(nc_file[datasetname].shape[2]/nprocs)
        num_cols_local = nc_file[datasetname].shape[2] - rank*num_cols_rank
        rval =  nc_file[datasetname][:,:,
                                rank*num_cols_rank:].reshape(-1,nc_file[datasetname].shape[1]*num_cols_local).T

    nc_file.close()
    return rval.filled()

# time test with mini-data parallel (2*8192 rows and 800 columns)
def test_mini_parallel(mini_files='data/mini_data/'):
    # Path to mini-data
    path = os.path.join(CFD, mini_files)
    
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nprocs = comm.Get_size()
    
    # Batchwise data - note these are 4 .h5 files
    data_list=[]
    for i in range(4):
        data_path = os.path.join(path, f'Batch_{i}_data.h5')
        data = load_h5_parallel(data_path,comm,rank,nprocs,'dataset')
        data_list.append(data)

    # Construct SVD objects
    ParSVD = ParSVD_Parallel(K=20, ff=1.0, low_rank=False)
    # Do first modal decomposition -- Parallel
    s = time.time()
    ParSVD.initialize(data_list[0])
    # Incorporate new data -- Parallel
    for i in range(1,4):
        ParSVD.incorporate_data(data_list[i])

    if ParSVD.rank == 0: print(f"Runing time for parallel calculation:{time.time() - s:.3f} seconds.")
   
def test_mini_serial(mini_files='data/mini_data/'):
    # Path to mini-data
    path = os.path.join(CFD, mini_files)
    
    # Batchwise data - note these are 4 .h5 files
    # import data from HDF5 file to create numpy arrays
    data_list=[]
    for i in range(4):
        data_path = os.path.join(path, f'Batch_{i}_data.h5')
        data= load_h5_serial (data_path,'dataset')
        data_list.append(data)
        
    SerSVD = ParSVD_Serial(K=10, ff=1.0)    
    start = time.time()
    SerSVD.initialize(data_list[0])
    # Incorporate new data -- serial
    for i in range(1,4):
        SerSVD.incorporate_data(data_list[i]) 
    print(f"Runing time for serial calculation: {time.time() - start:.3f} seconds.")

# test with random matrix:  
def test_random_parallel(random_files='data/data_generate/'):
    # Path to mini-data    
    path = os.path.join(CFD,random_files)
    
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nprocs = comm.Get_size()
        
    # Batchwise data - note these are 5 .h5 files
    data_list=[]
    for i in range(5):
        data_path = os.path.join(path, f'randommatrix_part_{i}.h5')
        data = load_h5_parallel(data_path,comm,rank,nprocs,'matrix')
        data_list.append(data)
    # Construct SVD objects
    ParSVD = ParSVD_Parallel(K=20, ff=1.0, low_rank=False)
    # Do first modal decomposition -- Parallel
    s = time.time()
    ParSVD.initialize(data_list[0])
    # Incorporate new data -- Parallel
    for i in range(1,5):
        ParSVD.incorporate_data(data_list[i])

    if ParSVD.rank == 0: print(f"Runing time for parallel calculatio:{time.time() - s:.3f} seconds.")
    
# test with download matrix in nc file:   
def test_downloadmatrix_parallel(filename):
    # Construct SVD objects
    ParSVD = ParSVD_Parallel(K=10, ff=1.0, low_rank=True)

    # Path to data
    data_path = os.path.join(CFD, filename)

    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nprocs = comm.Get_size()
    
    # Data from nc file
    initial_data = load_nc_parallel(data_path,comm,rank,nprocs,'sp')

    # Do first modal decomposition -- Parallel
    start = time.time()
    ParSVD.initialize(initial_data)

    # Incorporate new data -- Parallel
    if ParSVD.rank == 0:  print(f"Runing time for parallel calculation: {time.time() - start:.3f} seconds.")
