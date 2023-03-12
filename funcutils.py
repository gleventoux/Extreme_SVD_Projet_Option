# Import
import numpy as np
import h5py
import os
import csv
import timeit


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
    
    files = os.listdir(decomposition_dir) # files in decomposition_dir
    files.remove(".gitkeep") # we want delete all files execpt .gitkeep
    for file in files:
        file_path = os.path.join(decomposition_dir,file) # file path
        os.remove(file_path) # remove file


def timer(svd_func,matrix_filename,decomposition_dir, run_nbr=5, loader = None):
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
    TODO not sure how to handle different loading ways.
    loader : func, optional
        different functions to load matrices differently from hdf5 files 
        which use matrix_filename to return a numpy array for calculations.
        Default is None
    decomposition_dir : str
        the path to the directory where the decomposition is stored as matrixes in hdr5 format
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
    # timeit 
    times = timeit.repeat(lambda: svd_func(matrix_filename), repeat=run_nbr, number=1)
    avg_time = sum(times) / run_nbr
    # Clean up
    decompostion_cleaner(decomposition_dir=decomposition_dir)
    result = { (svd_func.__name__, matrix_filename): avg_time }
    return result
    
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

    with open(results_file, 'w', newline='') as csvfile:
        fieldnames = ['function', 'matrix', 'time'] # columns names in the .csv file
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() # write columns names
        for key in results.keys():
            function, matrix, time = key[0], key[1], results[key]
            writer.writerow({'function': function, 'matrix': matrix, 'time': time}) # fill .csv file
        

def hdf5_to_memmap(matrixname,rows,columns):

    filename = os.path.splitext(matrixname)[0]
    # TODO gérer les problèmes de path quand on est pas dans le répertoire courant
    target_memmap = np.memmap(filename+'.dat', dtype='float64',mode = 'w+',shape = (rows,columns))
    
    with h5py.File(matrixname,"r") as f:

        for (i,batch) in enumerate(f.keys()):
            batch_size= f[batch].shape[0]
            target_memmap[i:i+batch_size] = f[batch][:]
            target_memmap.flush()
    