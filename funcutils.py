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
        the path to the directory where the decomposition is stored as matrixes in hdf5 format

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

def dat_cleaner(matrix_dir):
    """
    Delete the numpy.memmaps stored in matrix_dir as .dat files

    Parameters
    ----------
    matrix_dir : str
        the relative path to the directory where the the numpy.memmaps stored as .dat files
    Returns
    -------
    None 
        Side effect of deleting the .dat files in matrix_dir

    """
    
    files = os.listdir(matrix_dir) # files in matrix_dir
    for file in files:
        if file.split('.')[-1]=='dat':
            file_path = os.path.join(matrix_dir,file) # file path
            os.remove(file_path) # remove file


def timer(svd_func,matrix_filename,kwargs,decomposition_dir, run_nbr=5):
    """
    Perform a timeit benchmark on a svd decomposition function 
    on a matrix stored at matrix_filename with run_nbr number of runs

    TODO Don't forget to clean the results of svd_func


    Parameters
    ----------
    svd_func : func
        the svd decomposition function, imported from svd_func.py
    matrix_filename : str
        the path to the stored matrix in an approriate format for svd_func
    kwargs = arguments of svd_function as a dictionnary 
    decomposition_dir : str
        the path to the directory where the decomposition is stored as matrixes in hdf5 format
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
    # Detection du type de stockage de matrix_filename

    # timeit 
    times = timeit.repeat(lambda: svd_func(matrix_filename, **kwargs), repeat=run_nbr, number=1)
    avg_time = sum(times) / run_nbr
    # Clean up
    decompostion_cleaner(decomposition_dir=decomposition_dir)
    matrix_name = os.path.split(matrix_filename)[-1].split('.')[0]
    result = { (svd_func.__name__, matrix_name): avg_time }
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

    with open(results_file, 'a', newline='') as csvfile:
        fieldnames = ['function', 'matrix', 'time'] # columns names in the .csv file
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() # write columns names
        for key in results.keys():
            func_name, matrix, time = key[0], key[1], results[key]
            writer.writerow({'function': func_name, 'matrix': matrix, 'time': time}) # fill .csv file
        

def hdf5_to_memmap(matrix_name,rows,columns):
    """
    Create a copy of a matrix stored in a .hdf5 format as a numpy.memmap stored in a .dat format.

    Parameters
    ----------
    matrix_name : str
        Relative path to the matrix stored in a .hdf5 format
    rows : int
        Number of rows of the matrix
    columns : 
        Number of columns of the matrix

    Returns
    -------
    filename : str
        Relative path to the .dat file representing the numpy.memmap
    
    """

    filename = os.path.splitext(matrix_name)[0]+'.dat'
    
    target_memmap = np.memmap(filename, dtype='float64',mode = 'w+',shape = (rows,columns))
    
    with h5py.File(matrix_name,"r") as f:

        for (i,batch) in enumerate(f.keys()):
            batch_size= f[batch].shape[0]
            target_memmap[i:i+batch_size] = f[batch][:]
            target_memmap.flush()
    return filename
    