# Import
import funcutils
import svd_func
import gc



# Matrix list definition
matrix_list = [] # list of string, each being the name of the file associated with an matrix, extension included

path_to_matrix_dir = '/matrix/' # Assume linux system path

matrix_list_with_dir = [ path_to_matrix_dir + matrix for matrix in matrix_list]

# Initialisation of global varaible and constants
benchmark_results = {}
NUMBER_OF_RUNS = 3

for matrix in matrix_list_with_dir :
    
    # TODO for each svd_decomposition function, 
    # write the following line adapted to each decomposition function
    results = funcutils.timer(svd_func.svd_func_template,matrix,run_nbr = NUMBER_OF_RUNS)
    benchmark_results.update(results)
    gc.collect()

funcutils.results_storer(benchmark_results,'benchmark_results.csv')

