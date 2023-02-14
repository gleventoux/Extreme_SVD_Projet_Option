# Import

def decompostion_cleaner(decomposition_dir):
    """
    Delete the result of an svd decomposition stored in decomposition_dir

    Parameters
    ----------
    decomposition_dir : str
        the path to the directory where the decomposition is stored as matrixes in hdr5 format

    Returns
    -------
    None 
        Side effect of deleting the files in decomposition_dir

    """


def timer(svd_func, matrix_filename, run_nbr=5):
    """
    Perform a timeit benchmark on a svd decomposition function 
    on a matrix stored at matrix_filename with run_nbr number of runs

    TODO Don't forget to clean the results of  svd_func


    Parameters
    ----------
    svd_func : func
        the svd decomposition function, imported from svd_func.py
    matrix_filename : str
        the path to the stored matrix in hdr5 format
    run_nbr : int, optional
        Number of time timeit performs the benchmark (default is 5)

    Returns
    -------
    result : dict
        a dictionnary of a singular key : value pair defined as
            key = (svd_fun_name, matrix_name) : tuple
                svd_fun_name : str
                matrix_name : str
            value = averaged benchmark time in s : float

    """
    



def results_storer(results, results_file):
    """
    Write the content of results in a .csv file with the first column designing the svd method,
    the second column the matrix name, the third column the matrix type, 
    the fourth column the benchmark results associated.
    Create such file if it does not already exist

    TODO define the columns names for an header at line 0
    

    Parameters
    ----------
    results : dict
        a dictionnary defined as { key : value } and 
            key = (svd_fun_name, matrix_name) : tuple
                svd_fun_name : str
                matrix_name : str
            value = averaged benchmark time in s : float
    results_file : str
        the path to the desired .csv file, include extension
    

    Returns
    -------
    None
        Side effect of writing a .csv file

    """
    