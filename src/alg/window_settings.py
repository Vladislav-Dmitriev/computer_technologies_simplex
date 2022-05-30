from PyQt5 import QtWidgets
from design_gui.design import Ui_MainWindow
import numpy as np
from matplotlib import pylab
from src.alg.exceptions import InputSimplexException, \
    SimplexAlgorithmException, NotSolveSimplexException, IncompleteTaskRankException, LoopingAlgorithmException
from src.alg.simplex.start_work import SimplexValues


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.comboBox_signs = ["=", ">=", "<="]
        self.comboBox_extreme = ["min", "max"]
        self.comboBox_columns_values = ['..', "2", "3", "4",
                                        "5", "6", "7"]
        self.comboBox_value_limits = ["any", "positive"]
        self.column_value_name = "X"
        self.column_right_part_name = "b"
        self.column_extreme_name = "extreme"
        self.start_ui()

    def start_ui(self):
        self.ui.comboBox_columns.addItems(self.comboBox_columns_values)  # columns num
        self.ui.comboBox_lines.addItems(self.comboBox_columns_values)  # lines num
        self.hide_labels()  # while don't enter dimensions we don't show A and c
        # buttons (send signal to...)
        self.ui.comboBox_lines.textActivated.connect(self.btn_clicked_dimensions)
        self.ui.comboBox_columns.textActivated.connect(self.btn_clicked_dimensions)
        self.ui.pushButton_solve_simplex.clicked.connect(
            self.btn_clicked_solve)
        self.ui.pushButton_plot.clicked.connect(self.plot_graphic)

    def hide_labels(self):
        self.ui.tableWidget_A.hide()
        self.ui.tableWidget_function.hide()
        self.ui.label_limitations.hide()
        self.ui.label_function.hide()
        self.ui.pushButton_solve_simplex.hide()
        self.ui.label__limit_value.hide()
        self.ui.tableWidget_limit_value.hide()
        self.ui.label_solve.hide()
        self.ui.label_error_message.hide()
        self.ui.pushButton_plot.hide()

    def clear_labels(self):
        self.ui.tableWidget_A.clear()
        self.ui.tableWidget_function.clear()
        self.ui.tableWidget_limit_value.clear()
        self.ui.label_error_message.clear()
        self.ui.label_solve.clear()

    def plot_graphic(self):
        figure = pylab.figure()
        axes = figure.add_subplot(1, 1, 1)
        min_x = -10
        max_y = 20
        delta = 0.1
        A, b = self.simplex_example.give_plot_dates()
        x_list = list(np.arange(min_x, max_y, delta))
        Y_lists = self.limit_functions(A, b, x_list)
        for i in range(self.M):
            pylab.plot(x_list, Y_lists[i])
        y_null_list = [x for x in x_list]
        x_null_list = [0 for i in range(len(y_null_list))]
        pylab.plot(x_null_list, y_null_list)
        arrowprops = {
            'arrowstyle': '->',
        }
        first_point = self.plot_points[0]
        solve_point = self.plot_points[-1]
        line_type = "x"
        for id, point in enumerate(self.plot_points):
            if id != 0:
                line_type = "h"
            pylab.plot(point[0], point[1], line_type)
        pylab.annotate(u'Initial approach',
                       xy=(first_point[0], first_point[1]),
                       xytext=(first_point[0] + 2, first_point[1] + 0.1),
                       arrowprops=arrowprops)
        pylab.annotate(u'decision',
                       xy=(solve_point[0], solve_point[1]),
                       xytext=(solve_point[0] + 2, solve_point[1] + 0.1),
                       arrowprops=arrowprops)
        axes.grid()
        pylab.show()

    def limit_functions(self, A, b, X):
        Y = [[0] * len(X) for _ in range(self.M)]
        for i in range(self.M):
            for id, x in enumerate(X):
                Y[i][id] = (-A[i][0] * x + b[i]) / A[i][1]
        return Y

    def btn_clicked_dimensions(self):
        self.clear_labels()  # need if a built something
        columns_box_date = self.ui.comboBox_columns.currentText()
        lines_box_date = self.ui.comboBox_lines.currentText()
        if columns_box_date.isdigit() and lines_box_date.isdigit():
            self.N = int(columns_box_date)
            self.M = int(self.ui.comboBox_lines.currentText())
        else:
            return
        self.build_table()  # build all widgets
        self.build_function()
        self.build_value_limit()
        self.ui.pushButton_solve_simplex.show()  # button "Посчиать"
        self.ui.pushButton_plot.hide()

    def build_table(self):
        self.ui.label_limitations.show()
        self.ui.tableWidget_A.show()
        self.ui.tableWidget_A.setColumnCount(self.N + 2)
        self.ui.tableWidget_A.setRowCount(self.M)
        self.ui.tableWidget_A.setHorizontalHeaderLabels(
            [self.column_value_name + str(i + 1) for i in range(self.N)] + [" ", self.column_right_part_name])
        combo = QtWidgets.QComboBox()
        combo.addItems(self.comboBox_signs)
        for i in range(self.M):
            self.ui.tableWidget_A.setCellWidget(i, self.N, combo)
            combo = QtWidgets.QComboBox()
            combo.addItems(self.comboBox_signs)

    def build_function(self):
        self.ui.label_function.show()
        self.ui.tableWidget_function.show()
        self.ui.tableWidget_function.setColumnCount(self.N + 1)
        self.ui.tableWidget_function.setRowCount(1)
        self.ui.tableWidget_function.setHorizontalHeaderLabels(
            [self.column_value_name + str(i + 1) for i in range(self.N)] + [self.column_extreme_name])
        combo = QtWidgets.QComboBox()
        combo.addItems(self.comboBox_extreme)
        self.ui.tableWidget_function.setCellWidget(0, self.N, combo)

    def build_value_limit(self):
        self.ui.label__limit_value.show()
        self.ui.tableWidget_limit_value.show()
        self.ui.tableWidget_limit_value.setColumnCount(self.N)
        self.ui.tableWidget_limit_value.setRowCount(1)
        self.ui.tableWidget_limit_value.setHorizontalHeaderLabels(
            [self.column_value_name + str(i + 1) for i in range(self.N)])
        combo = QtWidgets.QComboBox()
        combo.addItems(self.comboBox_value_limits)
        for i in range(self.N):
            self.ui.tableWidget_limit_value.setCellWidget(0, i, combo)
            combo = QtWidgets.QComboBox()
            combo.addItems(self.comboBox_value_limits)

    def constraint_matrix_A_filling(self):
        A = [[0] * self.N for _ in range(self.M)]
        for i in range(self.M):
            for j in range(self.N):
                try:
                    A[i][j] = float(self.ui.tableWidget_A.item(i, j).text())
                except Exception:
                    raise InputSimplexException(
                        object_name="coefficients for the constraint matrix.")
        return A

    def goal_function_coefficients_filling(self):
        c = [0 for _ in range(self.N)]
        for i in range(self.N):
            try:
                c[i] = float(self.ui.tableWidget_function.item(0, i).text())
            except Exception:
                raise InputSimplexException(
                    object_name="coefficients for goal function.")
        return c

    def signs_right_part_filling(self):
        signs = [0 for _ in range(self.M)]
        for i in range(self.M):
            signs[i] = self.ui.tableWidget_A.cellWidget(i, self.N) \
                .currentText()
        return signs

    def right_part_task_filling(self):
        b = [0 for _ in range(self.M)]
        for i in range(self.M):
            try:
                b[i] = float(self.ui.tableWidget_A.item(i, self.N + 1).text())
            except Exception:
                raise InputSimplexException(
                    object_name="the right side of the set of restrictions.")
        return b

    def constraint_values_filling(self):
        var_signs = [0 for _ in range(self.N)]
        for i in range(self.N):
            var_signs[i] = self.ui.tableWidget_limit_value. \
                cellWidget(0, i).currentText()
        return var_signs

    def extreme_goal_function_filling(self):
        return self.ui.tableWidget_function.cellWidget(0, self.N) \
            .currentText()

    def init_values_for_simplex(self):
        try:
            A = self.constraint_matrix_A_filling()
            c = self.goal_function_coefficients_filling()
            signs = self.signs_right_part_filling()
            b = self.right_part_task_filling()
            var_signs = self.constraint_values_filling()
            extreme = self.extreme_goal_function_filling()
        except InputSimplexException as exception:
            raise exception
        return c, extreme, A, signs, b, var_signs

    def print_error_message(self, exception):
        self.ui.label_solve.hide()
        self.ui.pushButton_plot.hide()
        self.ui.label_error_message.show()
        self.ui.label_error_message.setText(exception.message())
        self.ui.label_error_message.adjustSize()

    def print_solve_answer(self, result):
        self.ui.label_solve.show()
        self.ui.label_error_message.hide()
        self.ui.label_solve.setText("Answer: " + "  " + str(result))
        self.ui.label_solve.adjustSize()
        if self.N == 2:  # if 2 values then show on graphic
            self.ui.pushButton_plot.show()

    def btn_clicked_solve(self):
        try:
            simplex_dates = self.init_values_for_simplex()
        except InputSimplexException as exception:
            self.print_error_message(exception)
            return
        self.simplex_example = SimplexValues(*simplex_dates)

        try:
            result, self.plot_points = self.simplex_example.extreme_value()
        except (SimplexAlgorithmException, IncompleteTaskRankException, NotSolveSimplexException, LoopingAlgorithmException) as exception:
            self.print_error_message(exception)
            return

        self.print_solve_answer(result)
