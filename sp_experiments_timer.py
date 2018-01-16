import os
from timeit import default_timer as timer
import itertools
import pandas as pd
import numpy as np

experiments_list = ['gauss.py', 'rectangular.py',
                    'simpson.py', 'trapesoidal.py']

cpu_range = range(3, 4)

B_range = np.linspace(1.0, 7.5, 10)


def main():
    fp_exp_results = pd.DataFrame(
        columns=['Algorithm', 'Cores', 'N(b)', 'Integration_step', 'AVG_time'])
    cpu = 3
    for exp, b in itertools.product(experiments_list, B_range):
        avg_time = 0.0
        for i in range(25):
            start = timer()
            msg = os.system(
                "mpiexec -n {1} python3 /home/pavel/repos/mpi_lab/{0} 0.0 {2} 1 0.001".format(exp, cpu, b))
            end = timer()
            avg_time += end - start
        avg_time /= 25
        fp_exp_results = fp_exp_results.append(
            {'Algorithm': exp, 'Cores': cpu, 'AVG_time': avg_time, 'N(b)': b, 'Integration_step': 0.001}, ignore_index=True)
    fp_exp_results.to_csv('sp_experiment.csv', index=False)


if __name__ == '__main__':
    main()
