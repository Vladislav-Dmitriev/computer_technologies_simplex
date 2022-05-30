import sys
sys.path.append('../')
from PyQt5 import QtWidgets
from src.alg.window_settings import MyWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
    sys.exit(app.exec())