from PyQt5 import QtWidgets, QtCore
from QtWrapper import *
from views.ImagePreviewDialog import ImagePreviewDialog

fileTypesDictionary = {
    "Text File (*.txt)": "txt",
    "CSV (*.csv)": "csv"
}


class ExportFileDialog(QtWidgets.QDialog):

    def __init__(self, previewImages):
        super().__init__()
        self.leadPreviewImages = previewImages
        self.fileExportPath = None
        self.fileType = None
        self.setWindowTitle("Export ECG Data")
        self.resize(700, 400)  #arbitrary size - just set to this for development purposes
        self.buildUI()

    def buildUI(self):

        self.leadPreviewLayout = QtWidgets.QFormLayout()

        # Create label and preview button for each lead that was processed
        for leadId, image in sorted(self.leadPreviewImages.items(), key=lambda img: img[0].value):
            self.leadPreviewLayout.addRow(
                Label(owner=self, text="Lead " + str(leadId.name)),
                PushButton(owner=self, name="button", text="Preview")
            )
            self.button.clicked.connect(lambda checked, img=image.data, title=leadId.name: self.displayPreview(img, title))

        VerticalBoxLayout(owner=self, name="mainLayout", contents=[
            HorizontalBoxLayout(owner=self, name="chooseFileLayout", contents=[
                Label(
                    owner=self,
                    name="chooseFileLabel",
                    text="Export to:"
                ),
                LineEdit(
                    owner=self,
                    name="chooseFileTextBox",
                    contents="Choose file path",
                    readOnly=True
                ),
                PushButton(
                    owner=self,
                    name="chooseFileButton",
                    text="..."
                )
            ]),
            HorizontalBoxLayout(owner=self, name="delimiterChoiceLayout", contents=[
                    Label(
                        owner=self,
                        name="delimiterLabel",
                        text="Data Delimiter: "
                    ),
                    ComboBox(
                        owner=self,
                        name="delimiterDropdown",
                        items=[
                            "Comma",
                            "Tab",
                            "Space"
                        ]
                    )

            ]),
            VerticalBoxLayout(owner=self, name="leadPreviewLayout", contents=[
                Label(
                    owner=self,
                    name="leadPreviewLabel",
                    text="Preview Selected Leads:"
                ),
                ScrollArea(
                    owner=self,
                    name="leadPreivewScrollArea",
                    innerWidget=
                        Widget(
                            owner=self,
                            name="leadPreviewWidget",
                            layout=self.leadPreviewLayout
                        )
                )
            ]),
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
            ])
        ])

        self.delimiterChoiceLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.confirmCancelButtonLayout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

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
            self.accept()
        else:
            print("no export path selected")
            self.errorMessageLabel.setText("Please select a valid export path")

    def displayPreview(self, image, title):
        previewDialog = ImagePreviewDialog(image, title)
        previewDialog.exec_()
