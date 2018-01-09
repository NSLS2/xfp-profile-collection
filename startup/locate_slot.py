from string import ascii_uppercase
import numpy as np


NUM_COLS = 8
NUM_ROWS = 12

numbers = [str(x) for x in range(1, NUM_ROWS+1)]
letters = [x for x in ascii_uppercase[:NUM_COLS][::-1]]

l = np.array([letters] * NUM_ROWS)
n = np.array([numbers] * NUM_COLS).T

ln = np.core.defchararray.add(l, n)


def find_2d_index(arr, idx_ln):
    return np.argwhere(arr==idx_ln)[0]

def find_1d_index(arr, idx_ln):
    return np.argwhere(np.ravel(arr)==idx_ln)[0][0]

def find_element_by_1d_index(arr, idx_1d):
    return np.ravel(arr)[idx_1d]

def find_element_by_2d_index(arr, idx_2d):
    return arr[tuple(idx_2d)]

