import subprocess

num_processes = 4 
script_file = 'svd_func.py'  
cmd_list = ['mpirun', '-np', str(num_processes), 'python3', script_file]
result = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print(result.stdout.decode('utf-8'))
print(result.stderr.decode('utf-8'))