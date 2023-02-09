# Import
import funcutils
import svd_func
import gc



# Matrix list definition
matrix_list = [] # list of string, each being the name of the file associated with an matrix, extension included

# Initialisation of global varaible and constants
benchmark_results = {}
NUMBER_OF_RUNS = 3

for matrix in matrix_list :
    
    # TODO for each svd_decomposition function, write the following line 
    results = funcutils.timer(svd_func.svd_func_template,matrix,run_nbr = NUMBER_OF_RUNS)
    benchmark_results.update(results)

funcutils.results_storer(benchmark_results,'benchmark_results.csv')

