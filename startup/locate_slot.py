from string import ascii_uppercase


def find_2d_index(arr, idx_ln):
    """TODO: add docstrings

       arr: alpha-numeric 2D-array
    """
    return np.argwhere(arr==idx_ln.upper())[0]


def find_1d_index(arr, idx_ln):
    """TODO: add docstrings

       arr: alpha-numeric 2D-array
    """
    return np.argwhere(np.ravel(arr)==idx_ln.upper())[0][0]


def find_slot_by_2d_index(arr, idx_2d):
    """TODO: add docstrings

       arr: alpha-numeric 2D-array
    """
    return arr[tuple(idx_2d)]


def find_slot_by_1d_index(arr, idx_1d):
    """TODO: add docstrings

       arr: alpha-numeric 2D-array
    """
    return np.ravel(arr)[idx_1d]



NUM_COLS = 8
NUM_ROWS = 12

numbers = [str(x) for x in range(1, NUM_ROWS+1)]
letters = [x for x in ascii_uppercase[:NUM_COLS][::-1]]

l = np.array([letters] * NUM_ROWS)
n = np.array([numbers] * NUM_COLS).T

ln = np.core.defchararray.add(l, n)


