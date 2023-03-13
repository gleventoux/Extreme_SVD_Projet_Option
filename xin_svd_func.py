# Import
import os
import h5py
import numpy as np

# # num_processes = 4 
# # script_file = 'xin_svd_func.py'  
# # cmd_list = ['mpirun', '-np', str(num_processes), 'python3', script_file]
# # result = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# # print(result.stdout.decode('utf-8'))
# # print(result.stderr.decode('utf-8'))

# __file__ = "<path_to_file>"
# CWD = os.getcwd()
# CF  = os.path.realpath(__file__)
# CFD = os.path.dirname(CF)

# # Import library specific modules
# # sys.path.append(os.path.join("./"))
from pyparsvd.parsvd_serial   import ParSVD_Serial
from pyparsvd.parsvd_parallel import ParSVD_Parallel

# decomposition_dir=os.path.join(CFD,'decomposition_results')
# Matrix=os.path.join(CFD,"matrix") 


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
        Naming convention : - SVD_Method_Matrix_Name_U : Left Singular Vectors
                            - SVD_Method_Matrix_Name_S : Singular Values (1D Vector if possible)
                            - SVD_Method_Matrix_Name_V : Right Singular Vectors


   """
    pass


# method for importing data from .h5 files into the forms suitable for pyparsvd serial calculation
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
    dataset = dataset[:,:].reshape(dataset.shape[0],-1)
    h5_file.close()
    return dataset


# method for importing data from .h5 files into the forms suitable for parallel calculation and use mpi for IO acceleration
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

# data_list is generated from data_splitter.py data_splitter()
def pypar_serial(filename, results_dir,random=False,K=10,ff=1.0):
    SerSVD = ParSVD_Serial(K=K, ff=ff,low_rank=random,results_dir=results_dir)  
    data_list=filename.copy()  
    data_init=data_list.pop(0)
    data_init=load_h5_serial(data_init,'dataset')
    SerSVD.initialize(data_init)
    print('initialization successful')
    del data_init
    for i,data in enumerate(data_list):
        data=load_h5_serial(data,'dataset')
        SerSVD.incorporate_data(data)
        print(f'iteration {i+1} successful')
        del data 
    SerSVD.save()
    
# data_list is generated from data_splitter.py data_splitter()
def pypar_parallel(filenames, results_dir,random=False,K=10,ff=1.0):
    ParSVD = ParSVD_Parallel(K=K, ff=ff, low_rank=random,results_dir=results_dir)
    data_list=filenames.copy()
    data_init=data_list.pop(0)
    data_init=load_h5_parallel(data_init,ParSVD.comm,ParSVD.rank,ParSVD.nprocs,'dataset')
    ParSVD.initialize(data_init)
    if ParSVD.rank == 0:
        print('initialization successful')
    del data_init
    for i,data in enumerate(data_list):
        data=load_h5_parallel(data,ParSVD.comm,ParSVD.rank,ParSVD.nprocs,'dataset')
        ParSVD.incorporate_data(data)
        if ParSVD.rank == 0:
            print(f'iteration {i+1} successful')
        del data
        
    if ParSVD.rank == 0:
        ParSVD.save()
    
if __name__ == '__main__':
    data_list = list()
    tar_dir = Matrix
    filename= 'random1Go.hdf5'
    for iteration in range(5):
        data_list.append(os.path.join(tar_dir,f'splitted_{filename}_'+str(iteration)+'.h5'))
    #print(data_list)
    #pypar_serial(data_list)
    pypar_parallel(data_list,random=True)
    