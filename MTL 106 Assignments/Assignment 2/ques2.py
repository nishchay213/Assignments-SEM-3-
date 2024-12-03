import time as t
"""

Use the following function to convert the decimal fraction of k/N into it's binary representation
using k_prec number of bits after the decimal point. You may assume that the expansion of 
k/N terminates before k_prec bits after the decimal point.
"""
import numpy as np


# def decimalToBinary(num, k_prec) :
#
#     binary = ""
#     Integral = int(num)
#     fractional = num - Integral
#
#     while (Integral) :
#         rem = Integral % 2
#         binary += str(rem);
#         Integral //= 2
#
#     binary = binary[ : : -1]
#     binary += '.'
#
#     while (k_prec) :
#         fractional *= 2
#         fract_bit = int(fractional)
#
#         if (fract_bit == 1) :
#             fractional -= fract_bit
#             binary += '1'
#         else :
#             binary += '0'
#         k_prec -= 1
#
#     return binary


def win_probability(p, q, k, N):
    """
    Return the probability of winning while gambling aggressively.
    """
    if k >= N:
        return 1
    elif k == 0:
        return 0


    X =np.zeros((N+1,N+1))
    X[0][0]=1
    X[N][N]=1

    for i in range(1,N):
        if i<N/2:
            X[i][0]=q
            X[i][min(2*i,N)]=p
        else:
            X[i][N]=p
            X[i][2*i-N]=q

    Y = np.zeros(N+1)
    Y[N]=1

    Z = np.eye(N+1)-X
    Z[0]=0
    Z[0][0]=1
    Z[N]=0
    Z[N][N]=1

    return np.linalg.solve(Z,Y)[k]





def game_duration(p, q, k, N):
    """
    Return the expected number of rounds to either win or get ruined while gambling aggressively.
    """

    if k == 0:
        return 0
    elif k == N:
        return 0

    else:
        X = np.zeros((N+1,N+1))
        X[0][0]=1
        X[N][N]=1

        for i in range(1,N):
            if i<N/2:
                X[i][0]=q
                X[i][min(2*i,N)]=p
            else:
                X[i][N]=p
                X[i][2*i-N]=q

        Y = np.ones(N+1)
        Y[0]=0
        Y[N]=0

        Z = np.eye(N+1)-X
        Z[0]=0
        Z[0][0]=1
        Z[N]=0
        Z[N][N]=1

        return np.linalg.solve(Z,Y)[k]



