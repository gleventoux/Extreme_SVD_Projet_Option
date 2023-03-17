# Import
import funcutils
import svd_func
import xin_svd_func
import os

# locate the path to the target_directory for pyparsvd
__file__ = "<path_to_file>"
CF  = os.path.realpath(__file__)
CFD = os.path.dirname(CF)
tar_dir=os.path.join(CFD,"matrix") 

# Initialisation of global varaible and constants
benchmark_results = {}
NUMBER_OF_RUNS = 3
decomposition_dir = './decomposition_results/'

# Matrix list definition
matrix_list = ['random1Go.hdf5','petite.hdf5'] # list of string, each being the name of the file associated with an matrix, extension included
args_numpy = {'random1Go.hdf5':{'rows' : 25000, 'columns':5000, 'decomposition_dir':decomposition_dir},
              'petite.hdf5':{'rows' : 1000, 'columns':100, 'decomposition_dir':decomposition_dir}}
              
args_standard = { 'petite.hdf5':{ 'decomposition_dir':decomposition_dir}}

args_prepare_pypar= {'random1Go.hdf5':{'matrix_filename':'random1Go.hdf5','tar_dir':tar_dir,'niters':5,'nb_cols':5000},
                     'petite.hdf5':{'matrix_filename':'petite.hdf5','tar_dir':tar_dir,'niters':5,'nb_cols':5000}}
args_pypar_serial = {'random1Go.hdf5': {'results_dir': decomposition_dir,'random':False,'K':10,'ff':1.0},
                     'petite.hdf5':{'results_dir': decomposition_dir,'random':False,'K':10,'ff':1.0}}
args_pypar_parallel =  {'random1Go.hdf5': {'results_dir': decomposition_dir,'random':False,'K':10,'ff':1.0},
                     'petite.hdf5':{'results_dir': decomposition_dir,'random':False,'K':10,'ff':1.0}}

for matrix_name in matrix_list[1:] :
    
    matrix = os.path.join("matrix",matrix_name) # path to matrix file
    
    # TODO for each svd_decomposition function, 
    # write the following line adapted to each decomposition function
    
    # Numpy memmap streaming & Numpy SVD
    # matrix_memmap_filename = funcutils.hdf5_to_memmap(matrix, args_numpy[matrix_name]['rows'],args_numpy[matrix_name]['columns'])
    # results = funcutils.timer(svd_func.svd_numpy_naive, matrix_memmap_filename,args_numpy[matrix_name],decomposition_dir,run_nbr = NUMBER_OF_RUNS)
    # benchmark_results.update(results)
    # funcutils.dat_cleaner('./matrix/')

    # prepare of matrix
    filename_list = xin_svd_func.prepare_pypar(**args_prepare_pypar[matrix_name])

    # PyParSerial
    results = funcutils.timer(xin_svd_func.pypar_serial,filename_list, args_pypar_serial[matrix_name],decomposition_dir,run_nbr = NUMBER_OF_RUNS)
    benchmark_results.update(results)

    # PyParParallel
    results = funcutils.timer(xin_svd_func.pypar_parallel, filename_list,args_pypar_parallel[matrix_name],decomposition_dir,run_nbr = NUMBER_OF_RUNS)
    benchmark_results.update(results)
    funcutils.cleaner(matrix,filename_list)
    
    # Dask
    # results = funcutils.timer(svd_func.svd_dask, matrix, args_standard[matrix_name], decomposition_dir)
    # benchmark_results.update(results)

    # # Sklearn IPCA
    # results = funcutils.timer(svd_func.svd_sklearn, matrix, args_standard[matrix_name], decomposition_dir)
    # benchmark_results.update(results)
    
# funcutils.results_storer(benchmark_results,'benchmark_results.csv')

