from generate import generate_random
from funcutils import hdf5_to_memmap, timer, results_storer, dat_cleaner
from svd_func import svd_numpy_naive
import os 

aspect_ratio = [0.1,0.5,1,2,10]
matrix_sizes = [(3*(10**x), (10**x)) for x in range(0,5)]
matrix_paths = []

benchmark_results = {}
NUMBER_OF_RUNS = 3
decomposition_dir = './decomposition_results/'

for row,col in matrix_sizes:
    print(f"Matrice de taille {row}x{col}")
    matrix_name = f"rd_{row}x{col}"
    generate_random(matrix_name,row,col)
    matrix_path = file_path = os.path.join("matrix",matrix_name) + ".hdf5"
    matrix_paths.append(matrix_path)
    arg = {'rows' : row, 'columns':col, 'decomposition_dir':decomposition_dir}
    matrix_memmap_filename = hdf5_to_memmap(matrix_path, row,col)
    results = timer(svd_numpy_naive, matrix_memmap_filename,arg,decomposition_dir,run_nbr = NUMBER_OF_RUNS)
    benchmark_results.update(results)
    dat_cleaner('./matrix/')

results_storer(benchmark_results,'memmap_results.csv')



