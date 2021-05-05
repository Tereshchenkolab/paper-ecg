from PyQt5 import QtCore, QtGui, QtWidgets
from QtWrapper import *

class MessageDialog(QtWidgets.QDialog):
    def __init__(self, message="", title=""):
        super().__init__()
        self.message = message
        self.title = title
        self.initUI()
        self.connectUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        VerticalBoxLayout(owner=self, name="mainLayout", contents=[
            Label(
                owner=self,
                name="message",
                text=self.message
            ),
            PushButton(
                owner=self,
                name="okButton",
                text="OK"
            )
        ]
        )
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.mainLayout)

    def connectUI(self):
        self.okButton.clicked.connect(lambda: self.close())
