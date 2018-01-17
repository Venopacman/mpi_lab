import os
from timeit import default_timer as timer
import itertools
import pandas as pd

experiments_list = ['gauss.py', 'rectangular.py',
                    'simpson.py', 'trapesoidal.py']

cpu_range = range(1, 6)


def main():
    fp_exp_results = pd.DataFrame(columns=['Algorithm', 'Cores', 'time'])
    for exp, cpu in itertools.product(experiments_list, cpu_range):
        for i in range(40): 
            start = timer()
            msg = os.system(
                "mpiexec -n {1} python {0} 0.0 1.0 1000000 None".format(exp, cpu))
            end = timer()
            fp_exp_results = fp_exp_results.append(
                {'Algorithm': exp, 'Cores': cpu, 'time': timer() - start}, ignore_index=True)

    fp_exp_results.to_csv('fp_experiment_local_v2.csv', index=False)


if __name__ == '__main__':
    main()