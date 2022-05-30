import numpy as np
from src.alg.simplex.config import SimplexConfig


class LinearProgramProblem:
    def __init__(self, c, extr, A, signs, b, var_sings):
        self.c = c  # c - goal function coefficients
        self.extr = extr
        self.A = A  # A - constraint matrix
        self.signs = signs  # signs - signs between A and b
        self.b = b  # b - right part
        self.var_signs = var_sings  # limits on values
        self.lim_cnt, self.var_cnt = self.A.shape
        self.conf_X = list([i] for i in range(self.var_cnt))

    def convert_canon_type(self):
        self.convert_extr()
        self.convert_limit_sign()
        self.convert_var_sign()
        self.convert_b_sign()
        return self.A, self.b, self.c

    def convert_extr(self):
        if self.extr == SimplexConfig.maximum:
            self.c = (-1) * self.c
            self.extr = SimplexConfig.minimum

    def convert_limit_sign(self):
        for ind, sign in enumerate(self.signs):
            if sign == SimplexConfig.loose_less or sign == SimplexConfig.loose_more:
                self.var_signs.append(SimplexConfig.positive)
                self.var_cnt += 1
                self.c = np.append(self.c, 0)
                self.A = np.append(
                    self.A, np.zeros((self.lim_cnt, 1), float), axis=1)
                if sign == SimplexConfig.loose_less:
                    self.A[ind][self.var_cnt - 1] = 1
                if sign == SimplexConfig.loose_more:
                    self.A[ind][self.var_cnt - 1] = -1
                self.signs[ind] = SimplexConfig.equal

    def convert_var_sign(self):
        for ind, var in enumerate(self.var_signs):
            if var == SimplexConfig.any:
                self.var_signs[ind] = SimplexConfig.positive
                self.var_signs.append(SimplexConfig.positive)
                self.conf_X[ind].append(self.var_cnt)
                self.var_cnt += 1
                self.c = np.append(self.c, self.c[ind] * (-1))
                self.A = np.append(
                    self.A, np.array(
                        [[(-1) * self.A[j, ind]] for j in range(
                            self.lim_cnt)], float), axis=1)

    def convert_b_sign(self):
        for ind, var in enumerate(self.b):
            if var < 0:
                self.b[ind] *= (-1)
                self.A[ind] = (-1) * self.A[ind]

    def sort_conditions(self):
        for ind, sign in enumerate(self.signs):
            if (sign == SimplexConfig.loose_less and self.extr == SimplexConfig.minimum) or \
                    (sign == SimplexConfig.loose_more and self.extr == SimplexConfig.maximum):
                self.A[ind] *= (-1)
                self.b[ind] *= (-1)
                if sign == SimplexConfig.loose_less:
                    self.signs[ind] = SimplexConfig.loose_more
                elif sign == SimplexConfig.loose_more:
                    self.signs[ind] = SimplexConfig.loose_less

    def find_init_X(self, X):
        init_X = np.zeros(len(self.conf_X))
        for ind, nums in enumerate(self.conf_X):
            if len(nums) == 1:
                init_X[ind] = X[nums[0]]
            elif len(nums) == 2:
                init_X[ind] = X[nums[0]] - X[nums[1]]
        return init_X
