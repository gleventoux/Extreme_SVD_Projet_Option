# Import
import numpy as np
import h5py


def svd_func_template(matrix_filename, decomposition_dir,vectors = True):
    """
    Perform a svd decomposition on a matrix stored at matrix_filename 

    Parameters
    ----------
    matrix_filename : str
        the path to the stored matrix in hdr5 format
    decomposition_dir : str
        path to the directory, where the singular values and right and left singular vecors are stored
        in hdr5 format
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

def svd_numpy_naive(matrix_filename,rows,columns,decomposition_dir,vectors = True):
    """
    Perform a svd decomposition on a matrix stored at matrix_filename 

    Parameters
    ----------
    matrix_filename : str
        the path to the stored matrix in .dat format as a numpy.memmap
    decomposition_dir : str
        path to the directory, where the singular values and right and left singular vecors are stored
        in .dat format as a numpy.memmap
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

    k = min(rows,columns)
    outputname = decomposition_dir+'SVD_numpy_'
    #TODO gérer les problèmes de path

    a = np.memmap(matrix_filename,dtype = 'float64',mode = 'w+',shape = (rows,columns))
    s = np.memmap(outputname+'S.dat',dtype = 'float64',mode = 'w+',shape = k)
    if vectors:
        u = np.memmap(outputname+'U.dat',dtype = 'float64',mode = 'w+',shape = (rows,k))
        v = np.memmap(outputname+'V.dat',dtype = 'float64',mode = 'w+',shape = (k,columns))
        u[:],s[:],v[:] = np.linalg.svd(a,full_matrices=False, compute_uv=vectors) 
        u.flush()
        v.flush()
    else :
        s[:] = np.linalg.svd(a,full_matrices=False, compute_uv=vectors) 
    s.flush()
    

    