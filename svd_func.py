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

def pypar_serial(matrix_filename, decomposition_dir,random=False,vectors = True):
    pass

def pypar_parallel(matrix_filename, decomposition_dir,random=False,vectors = True):
    pass


    