import os
from timeit import default_timer as timer
import itertools
import pandas as pd

experiments_list = ['gauss.py', 'rectangular.py',
                    'simpson.py', 'trapesoidal.py']

cpu_range = range(1, 9)


def main():
    fp_exp_results = pd.DataFrame(columns=['Algorithm', 'Cores', 'AVG_time'])
    for exp, cpu in itertools.product(experiments_list, cpu_range):
        avg_time = 0.0
        for i in range(25):
            start = timer()
            msg = os.system(
                "mpiexec -n {1} python3 /home/pavel/repos/mpi_lab/{0} 0.0 1.0 30000 None".format(exp, cpu))
            end = timer()
            avg_time += end - start
        avg_time /= 25
        fp_exp_results = fp_exp_results.append(
            {'Algorithm': exp, 'Cores': cpu, 'AVG_time': avg_time}, ignore_index=True)
    fp_exp_results.to_csv('fp_experiment.csv', index=False)


if __name__ == '__main__':
    main()
