import os
from timeit import default_timer as timer
import itertools
import pandas as pd
import numpy as np

experiments_list = ['gauss.py', 'rectangular.py',
                    'simpson.py', 'trapesoidal.py']

B_range = np.linspace(1.0, 10.0, 40)


def main():
    fp_exp_results = pd.DataFrame(
        columns=['Algorithm', 'Cores', 'N(b)', 'Integration_step', 'AVG_time'])
    cpu = 8
    for exp, b in itertools.product(experiments_list, B_range):
        for i in range(40):
            start = timer()
            msg = os.system(
                "mpiexec -q -n {1} python3 /home/psmirnov/repos/mpi_lab/{0} 0.0 {2} 1 0.0005 ".format(exp, cpu, b))
            fp_exp_results = fp_exp_results.append(
                {'Algorithm': exp, 'Cores': cpu, 'time': timer() - start, 'N(b)': b, 'Integration_step': 0.001}, ignore_index=True)
    fp_exp_results.to_csv('sp_experiment_cluster.csv', index=False)


if __name__ == '__main__':
    main()
