import sys
import unittest

sys.path.append('../')

from tests.dates.test_dates import give_four_dim, give_two_dim
from src.alg.simplex.simplex_method import start_simplex_method
from src.alg.simplex.lin_prog_problem import LinearProgramProblem, np
import copy as cp


def solve(*example_dates):
    lp = LinearProgramProblem(*example_dates)
    canon_lp = cp.deepcopy(lp)
    canon_lp.convert_canon_type()
    X, plot_points = start_simplex_method(canon_lp.A, canon_lp.b,
                                          canon_lp.c)
    result_X_example = canon_lp.find_init_X(X)
    decision_example: float = float(np.dot(lp.c.transpose(), result_X_example))
    return round(decision_example, 1)


class TestGui(unittest.TestCase):

    def test_four_dim(self):
        self.assertEqual(solve(*give_four_dim()), 48.5)

    def test_two_dim(self):
        self.assertEqual(solve(*give_two_dim()), 16.4)


if __name__ == '__main__':
    unittest.main()
