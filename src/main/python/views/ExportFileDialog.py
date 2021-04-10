from PyQt5 import QtGui, QtWidgets, QtCore
from QtWrapper import *

fileTypesDictionary = {
    "Text File (*.txt)": "txt",
    "CSV (*.csv)": "csv"
}

class ExportFileDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__()
        self.editorWidget = parent
        self.fileExportPath = None
        self.fileType = None
        self.setWindowTitle("Export ECG Data")
        self.resize(700, 400)  #arbitrary size - just set to this for development purposes
        self.buildUI()

    def buildUI(self):
        self.mainLayout = QVBoxLayout()

        self.chooseFileLayout = QHBoxLayout()
        self.chooseFileLayout.addWidget(
            Label(
                owner=self,
                name="chooseFileLabel",
                text="Export to:"
            )
        )
        self.chooseFileLayout.addWidget(
            LineEdit(
                owner=self,
                name="chooseFileTextBox",
                contents="Choose file path"
            )
        )
        self.chooseFileTextBox.setReadOnly(True)    # idk if we want to leave this as read-only but I figured it makes one less thing to error handle at the moment
        self.chooseFileLayout.addWidget(
                PushButton(
                owner=self,
                name="chooseFileButton",
                text="..."
            )
        )

        self.mainLayout.addLayout(self.chooseFileLayout)
        
        HorizontalBoxLayout(owner=self, name="confirmCancelButtonLayout", contents=[
                Label(
                    owner=self,
                    name="errorMessageLabel",
                    text=""
                ),
                PushButton(
                    owner=self,
                    name="confirmButton",
                    text="Export"
                ),
                PushButton(
                    owner=self,
                    name="cancelButton",
                    text="Cancel"
                )
            ]
        )
        self.confirmCancelButtonLayout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.errorMessageLabel.
        self.mainLayout.addLayout(self.confirmCancelButtonLayout)

        self.setLayout(self.mainLayout)

        self.connectUI()

    def connectUI(self):
        self.chooseFileButton.clicked.connect(lambda: self.openSaveFileDialog())
        self.confirmButton.clicked.connect(lambda: self.confirmExportPath())
        self.cancelButton.clicked.connect(lambda: self.close())

    def openSaveFileDialog(self):
        path, selectedFilter = QtWidgets.QFileDialog.getSaveFileName(
                parent=self, 
                caption="Export to File",
                filter="Text File (*.txt);;CSV (*.csv)"
        )
        if path is not "" and selectedFilter in fileTypesDictionary:
            self.errorMessageLabel.setText("")
            self.chooseFileTextBox.setText(path)
            self.fileExportPath = path
            self.fileType = fileTypesDictionary[selectedFilter]

    def confirmExportPath(self):
        if self.fileExportPath is not None and self.fileType is not None:
            self.editorWidget.exportPathChosen.emit(self.fileExportPath, self.fileType)
        else:
            print("no export path selected")
            self.errorMessageLabel.setText("Please select a valid export path")
