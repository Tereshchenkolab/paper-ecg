from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets
from PyQt5 import uic
from utility import *

import os, sys

# class MainWindow(QtWidgets.QMainWindow):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.setWindowTitle("PyQt")
#         l = QtWidgets.QLabel(helloWorld())
#         l.setMargin(60)
#         self.setCentralWidget(l)

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    # Translate asset paths to useable format for PyInstaller
    def resource(relativePath):
      return appctxt.get_resource(relativePath)

    # window = MainWindow()
    # window.resize(250, 150)
    # window.show()

    Form, Window = uic.loadUiType(resource("qt/demo.ui"))
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)