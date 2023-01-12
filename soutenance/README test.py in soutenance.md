README test.py in soutenance

Before execute test.py:
  - install sklearn, h5py, dask, primme, line_profiler (pip install <pkg>)
  - Modify filename with the name of the .h5py storing the matrix (line 145 in test.py)
  - matrices (in .h5py format) must be placed in soutenance folder
  (to generate random matrice see readme)
  
Then execute with the cmd : python3 -m test (in folder soutenance)

See results with cmd : kernprof -l test.py, then python -m line_profiler test.py.lprof