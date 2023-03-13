# Import
import funcutils
import svd_func
import gc
import os

# Initialisation of global varaible and constants
benchmark_results = {}
NUMBER_OF_RUNS = 3
decomposition_dir = './decomposition_results/'

# Matrix list definition
matrix_list = ['random1Go.hdf5'] # list of string, each being the name of the file associated with an matrix, extension included
args_numpy= {'random1Go.hdf5':{'rows' : 25000, 'columns':5000, 'decomposition_dir':decomposition_dir}}


for matrix in matrix_list :
    
    matrix = os.path.join("matrix",matrix) # path to matrix file
    
    # TODO for each svd_decomposition function, 
    # write the following line adapted to each decomposition function
    
    results = funcutils.timer(svd_func.svd_numpy_naive, matrix,args_numpy[matrix],decomposition_dir,run_nbr = NUMBER_OF_RUNS)
    benchmark_results.update(results)
    gc.collect()

funcutils.results_storer(benchmark_results,'benchmark_results.csv')

