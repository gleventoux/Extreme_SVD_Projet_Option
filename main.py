# Import
import funcutils
import xin_svd_func
import gc
import os

# Matrix list definition
matrix_list = ['random1Go.hdf5'] # list of string, each being the name of the file associated with an matrix, extension included

# Initialisation of global varaible and constants
benchmark_results = {}
NUMBER_OF_RUNS = 3

for matrix in matrix_list :
    
    matrix = os.path.join("matrix",matrix) # path to matrix file
    
    # TODO for each svd_decomposition function, 
    # write the following line adapted to each decomposition function
    results = funcutils.timer(xin_svd_func.svd_func_template,matrix,run_nbr = NUMBER_OF_RUNS)
    benchmark_results.update(results)
    gc.collect()

funcutils.results_storer(benchmark_results,'benchmark_results.csv')

