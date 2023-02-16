# Import
import os
import sys
import numpy as np
from mpi4py import MPI
import h5py

# Define the __file__ global variable
__file__ = "<path_to_file>"
# Current, parent and file paths
CWD = os.getcwd()
CF  = os.path.realpath(__file__)
CFD = os.path.dirname(CF)

# Import library specific modules
# sys.path.append(os.path.join("./"))
from pyparsvd.parsvd_serial   import ParSVD_Serial
from pyparsvd.parsvd_parallel import ParSVD_Parallel

def svd_func_template(matrix_filename, decomposition_dir,vectors = True):
    """
    Perform a svd decomposition on a matrix stored at matrix_filename 

    Parameters
    ----------
    matrix_filename : str
        the path to the stored matrix in hdf5 format
    decomposition_dir : str
        path to the directory, where the singular values and right and left singular vecors are stored
        in hdf5 format
    vectors : bool, optional
        Boolean enabling the return of the right and left singular vectors
        (default is True)

    Returns
    -------
    None
        Side effect of writing the singular values and right and left singular vecors 
        in the directory at decomposition_dir in an hdr5 format


   """



# method for importing data from .h5 files into the forms suitable for pyparsvd serial calculation
def load_split(filename,datasetname,split=5):
    """
    Our matrix is stored in an HDF5 file with nb of batch
    This code loads a dataset from an HDF5 file 
    return a list of numpy array form data suitable for serial calculation
    
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
    

    # 获取数据集数量
    num_datasets = len(h5_file.keys())

    # 初始化数组
    matrix = np.empty((25000, 0), dtype=np.float32)

    # 逐个读取数据集
    for i in range(num_datasets):
        dataset = f['dataset{}'.format(i)]
        data = dataset[:]

        # 将数据添加到数组中
        matrix = np.hstack((matrix, data))

    # 将每个列分割成5部分
    num_columns = matrix.shape[1]
    split_columns = np.array_split(matrix, 5, axis=1)

    # 打印每个数组的形状
    for i, arr in enumerate(split_columns):
        print('Split array {}: {}'.format(i, arr.shape))
    
    
    
    return dataset

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
    num_rows_rank = int(ndof/nprocs)
    if rank != nprocs-1:
        rval =  dset[rank*num_rows_rank:(rank+1)*num_rows_rank,:].reshape(num_rows_rank,-1)
    else:
        num_dof_local = ndof - rank*num_rows_rank
        rval =  dset[rank*num_rows_rank:,:].reshape(num_dof_local,-1)
    h5_file.close()
    return rval

def pypar_serial(matrix_filename, decomposition_dir,split=5,random=False,vectors = True):
    
    pass




def pypar_parallel(matrix_filename, decomposition_dir,random=False,vectors = True):
    
    pass


    
if __name__ == '__main__':
    pypar_serial()
    pypar_parallel()
    