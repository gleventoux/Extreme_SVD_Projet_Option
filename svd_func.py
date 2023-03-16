# Import
import os
import h5py
import numpy as np
import dask.array as da
from sklearn.decomposition import IncrementalPCA

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


def svd_numpy_naive(matrix_filename, rows, columns, decomposition_dir ,vectors = True):
    """
    Perform a svd decomposition on a matrix stored at matrix_filename 

    Parameters
    ----------
    matrix_filename : str
        the path to the stored matrix in hdf5 format
    rows : int 
        number of rows of the matrix
    columns : int 
        number of columns of the matrix
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
    k = min(rows,columns)
    matrix_name = 'SVD_numpy_'+os.path.split(matrix_filename)[-1].split(".")[0]+"_"
    outputname =  os.path.join(decomposition_dir,matrix_name) 

    a = np.memmap(matrix_filename,dtype = 'float64',mode = 'c',shape = (rows,columns))
    s = np.memmap(outputname+'S.dat',dtype = 'float64',mode = 'w+',shape = k)
    if vectors:
        u = np.memmap(outputname+'U.dat',dtype = 'float64',mode = 'w+',shape = (rows,k))
        v = np.memmap(outputname+'V.dat',dtype = 'float64',mode = 'w+',shape = (k,columns))
        u[:],s[:],v[:] = np.linalg.svd(a,full_matrices=False, compute_uv=vectors) 
        u.flush()
        v.flush()
    else :
        s[:] = np.linalg.svd(a,full_matrices=False, compute_uv=vectors)[:]
    s.flush()


def svd_dask(matrix_filename, decomposition_dir, vectors = True):
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
    with h5py.File(matrix_filename, "r") as f:

        # get matrix name
        matrix_name = os.path.splitext(os.path.basename(matrix_filename))[0]

        # template for save files
        save_file_path_template = os.path.join(decomposition_dir,"SVD_Dask_" + matrix_name + "_{}.h5py")

        da_batch_list = [da.from_array(f[batch]) for batch in f.keys()]
        da_matrix = da.concatenate(da_batch_list)
        da_matrix = da.rechunk(da_matrix)
        
        # call the svd of dask
        u,s,v = da.linalg.svd(da_matrix)

        # compute singular values and save them
        s.compute()
        s.da.to_hdf5(save_file_path_template.format("S"),"s",s)

        if vectors:

            # compute and save left/right vectors
            u.compute()
            v.compute()
            u.da.to_hdf5(save_file_path_template.format("U"),"u",u)
            s.da.to_hdf5(save_file_path_template.format("V"),"v",v)


def svd_sklearn(matrix_filename, decomposition_dir, vectors = True):
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


    with h5py.File(matrix_filename,"r") as f:

        # get matrix name
        matrix_name = os.path.splitext(os.path.basename(matrix_filename))[0]

        # template for save files
        save_file_path_template = os.path.join(decomposition_dir,"SVD_IPCA_" + matrix_name + "_{}.h5py")

        ipca = IncrementalPCA()

        for batch in f.keys():
            ipca.partial_fit(f[batch])

        s = ipca.singular_values_

        with h5py.File(save_file_path_template.format("S"),'w') as f1:

            dset = f1.create_dataset("s",data=s)
    