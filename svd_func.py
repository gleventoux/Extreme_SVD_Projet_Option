# Import


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
                            - SVD_Method_Matrix_Name_S :  Singular Values (1D Vector if possible)
                            - SVD_Method_Matrix_Name_V : Right Singular Vectors

    """
    