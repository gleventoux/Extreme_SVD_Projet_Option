# Import
import funcutils
import svd_func
import xin_svd_func
import os

# Initialisation of global varaible and constants
benchmark_results = {}
NUMBER_OF_RUNS = 3
decomposition_dir = './decomposition_results/'

# Matrix list definition
matrix_list = ['random1Go.hdf5','petite.hdf5'] # list of string, each being the name of the file associated with an matrix, extension included
args_numpy = {'random1Go.hdf5':{'rows' : 25000, 'columns':5000, 'decomposition_dir':decomposition_dir},
              'petite.hdf5':{'rows' : 1000, 'columns':100, 'decomposition_dir':decomposition_dir}}
              
args_standard = { 'petite.hdf5':{ 'decomposition_dir':decomposition_dir}}
args_pypar_serial = {'random1Go.hdf5': 'foo'}
args_pypar_parallel = {'random1Go.hdf5': 'bar'}

for matrix_name in matrix_list[1:] :
    
    matrix = os.path.join("matrix",matrix_name) # path to matrix file
    
    # TODO for each svd_decomposition function, 
    # write the following line adapted to each decomposition function
    
    # Numpy memmap streaming & Numpy SVD
    matrix_memmap_filename = funcutils.hdf5_to_memmap(matrix, args_numpy[matrix_name]['rows'],args_numpy[matrix_name]['columns'])
    results = funcutils.timer(svd_func.svd_numpy_naive, matrix_memmap_filename,args_numpy[matrix_name],decomposition_dir,run_nbr = NUMBER_OF_RUNS)
    benchmark_results.update(results)
    funcutils.dat_cleaner('./matrix/')

    # # PyParSerial
    # prepared_stuff = xin_svd_func.prepare_pypar_serial(matrix, None, decomposition_dir=decomposition_dir)
    # results = funcutils.timer(xin_svd_func.pypar_serial, prepared_stuff,args_pypar_serial[matrix_name],decomposition_dir,run_nbr = NUMBER_OF_RUNS)
    # benchmark_results.update(results)
    # del prepared_stuff

    # # PyParParallel
    # prepared_stuff = xin_svd_func.prepare_pypar_parallel(matrix, None, decomposition_dir=decomposition_dir)
    # results = funcutils.timer(xin_svd_func.pypar_parallel, prepared_stuff,args_pypar_parallel[matrix_name],decomposition_dir,run_nbr = NUMBER_OF_RUNS)
    # benchmark_results.update(results)
    # del prepared_stuff

    # Dask
    results = funcutils.timer(svd_func.svd_dask, matrix, args_standard[matrix_name], decomposition_dir)
    benchmark_results.update(results)

    # Sklearn IPCA
    results = funcutils.timer(svd_func.svd_sklearn, matrix, args_standard[matrix_name], decomposition_dir)
    benchmark_results.update(results)

    funcutils.results_storer(benchmark_results,matrix_name+'_benchmark_results.csv')

