import sys

import numpy
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def f(x):
    return 4 / (1 + x**2)


def integrateRange(a, b, n):
    h = (b - a) / n
    integral = 0
    for i in range(1, int(n)):
        x = a + i * h
        integral += f(x - 0.5 * h) * h
    return integral


def main(glob_a, glob_b, glob_n):
    # h is the step-size
    h = (glob_b - glob_a) / glob_n

    local_n = glob_n / size

    # we calculate the interval that each process handles
    # local_a is the starting point and local_b is the endpoint
    local_a = glob_a + rank * local_n * h
    local_b = local_a + local_n * h

    # initializing variables. mpi4py requires that we pass numpy objects.
    integral = numpy.zeros(1)
    recv_buffer = numpy.zeros(1)

    # perform local computation. Each process integrates its own interval
    integral[0] = integrateRange(local_a, local_b, local_n)

    # communication
    # root node receives results from all processes and sums them
    if rank == 0:
        total = integral[0]
        for i in range(1, size):
            comm.Recv(recv_buffer, ANY_SOURCE)
            total += recv_buffer[0]
    else:
        # all other process send their result
        comm.Send(integral, 0)

    # root process prints results
    if comm.rank == 0:
        return "With n ={0} sub_integrals, our estimate of the integral from {1} to {2} is {3}".format(glob_n, glob_a, glob_b, total)


if __name__ == '__main__':
    glob_a = float(sys.argv[1])
    glob_b = float(sys.argv[2])
    glob_n = int(sys.argv[3])
    possible_h = str(sys.argv[4])
    if not possible_h.isalpha():
        # print('yea i now de decimol wey!')
        glob_n = (glob_b - glob_a) / float(possible_h)
        main(glob_a, glob_b, glob_n)
    else:
        # print('mi quin smth giz wrong!')
        main(glob_a, glob_b, glob_n)
