from PyQt5 import QtWidgets, QtCore
from ECGToolkit.Visualization import displayColorImage
from QtWrapper import *
from views.ImagePreviewDialog import ImagePreviewDialog
from ImageUtilities import opencvImageToPixmap


fileTypesDictionary = {
    "Text File (*.txt)": "txt",
    "CSV (*.csv)": "csv"
}


class ExportFileDialog(QtWidgets.QDialog):

    def __init__(self, parent, previewImages):
        super().__init__()
        self.leadPreviewImages = previewImages
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

        self.leadPreviewLayout = QtWidgets.QFormLayout()

        for leadId, image in self.leadPreviewImages.items():
            self.leadPreviewLayout.addRow(
                Label(
                    owner=self,
                    text="Lead " + leadId
                ),
                PushButton(
                    owner=self,
                    name="button",
                    text="Preview"
                )
            )
            self.button.clicked.connect(lambda checked, img=image, title=leadId: self.displayPreview(img, title))

        Widget(
            owner=self,
            name="leadPreviewWidget",
            layout=self.leadPreviewLayout
        )

        VerticalBoxLayout(owner=self, name="leadPreviewLayout", contents=[
            Label(
                owner=self,
                name="leadPreviewLabel",
                text="Preview Selected Leads:"
            ),
            ScrollArea(
                owner=self,
                name="leadPreivewScrollArea",
                innerWidget=self.leadPreviewWidget
            )
        ])

        self.mainLayout.addLayout(self.leadPreviewLayout)

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
            self.close()
        else:
            print("no export path selected")
            self.errorMessageLabel.setText("Please select a valid export path")

    def displayPreview(self, image, title):
        previewDialog = ImagePreviewDialog(image)
        previewDialog.exec_()

