from src.alg.simplex.lin_prog_problem import np


#  four dim task
# 2.0x0 + 3.0x1 + 1.0x2 + 5.0x3 -> max
# -2.0x0 + 6.0x1 + 1.0x2 + 0.0x3 <= 40.0
# 3.0x0 + 2.0x1 + 0.0x2 + 1.0x3 = 28.0
# 2.0x0 + -1.0x1 + 0.0x2 + 0.0x3 >= 14.0
# 1.0x0 + 2.0x1 + 4.0x2 + 1.0x3 = 12.0
# x1 >= 0
def give_four_dim():
    c = np.array([2, 3, 1, 5], float)
    extreme = 'max'
    A = np.array([[-2, 6, 1, 0],
                  [3, 2, 0, 1],
                  [2, -1, 0, 0],
                  [1, 2, 4, 1]], float)
    signs = ['<=', '=', '>=', '=']
    b = np.array([40, 28, 14, 12], float)
    var_signs = ['any', 'positive', 'any', 'any']
    return c, extreme, A, signs, b, var_signs


# two dim task
# 20.0x0 + 20.0x1 -> min
# 4.0x0 + 2.0x1 >= 2.0
# 6.0x0 + 3.0x1 >= 4.0
# 5.0x0 + 8.0x1 = 5.0
# x0 >= 0
# x1 >= 0
def give_two_dim():
    c = np.array([20, 20], float)
    extreme = 'min'
    A = np.array([[4, 2],
                  [6, 3],
                  [5, 8]], float)
    signs = ['>=', '>=', '=']
    b = np.array([2, 4, 5], float)
    var_signs = ['positive', 'positive']
    return c, extreme, A, signs, b, var_signs
