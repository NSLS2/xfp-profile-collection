import numpy as np
from string import ascii_uppercase

NUM_COLS = 8
NUM_ROWS = 12


class LetterNumberLocator:
    def __init__(self, num_cols=NUM_COLS, num_rows=NUM_ROWS):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self._numbers = [str(x) for x in range(1, num_rows+1)]
        self._letters = [x for x in ascii_uppercase[:num_cols][::-1]]
        self.letter_number_matrix = self._create_array()

    def find_1d_index(self, idx_ln):
        """
        Find 1d (flat) index by alpha-numeric code.

        Parameters
        ----------
        idx_ln : str
            alpha-numeric code, e.g. 'E4' (returns 27)
        """
        return np.argwhere(
            np.ravel(self.letter_number_matrix) == idx_ln.upper()
        )[0][0]

    def find_2d_index(self, idx_ln):
        """
        Find 2d index by alpha-numeric code.

        Parameters
        ----------
        idx_ln : str
            alpha-numeric code, e.g. 'E4' (returns [3, 3])
        """
        return np.argwhere(self.letter_number_matrix == idx_ln.upper())[0]

    def find_slot_by_1d_index(self, idx_1d):
        """
        Find slot's alpha-numeric value by 1d (flat) index.

        Parameters
        ----------
        idx_1d : int
            1d flat index, e.g. 27 (returns 'E4')
        """
        return np.ravel(self.letter_number_matrix)[idx_1d]

    def find_slot_by_2d_index(self, idx_2d):
        """
        Find slot's alpha-numeric value by 2d index.

        Parameters:
        -----------
        idx_2d : int
            2d index, e.g. [3, 3] (returns 'E4')
        """
        return self.letter_number_matrix[tuple(idx_2d)]

    def _create_array(self):
        letter = np.array([self._letters] * self.num_rows)
        number = np.array([self._numbers] * self.num_cols).T
        return np.core.defchararray.add(letter, number)


# if __name__ == '__main__':
#     letter_number = LetterNumberLocator()
