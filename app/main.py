from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtWidgets import QWidget, QCheckBox, QLabel, QPushButton, QFileDialog, QMessageBox
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtGui import Qt
from pathlib import Path
from .entities.file import File
from .entities.sheets import Sheets


import sys, shutil

class UserInterface(QWidget):
    def __init__(self) -> QWidget:
        super().__init__()

        self.__selectedTypeFile: str = '.zip';
        self.__selectedFile: File;

        self.__ui()
        self.__signal()

    def __ui(self):
        layout: QVBoxLayout = QVBoxLayout()
        legenda_arquivos: QLabel = QLabel("Formato dos arquivos")
    
        self.cbx_zip: QCheckBox = QCheckBox(".zip")
        self.cbx_zip.setChecked(True)
        self.cbx_xml: QCheckBox = QCheckBox(".xml")

        self.btn_selecionar_arquivo: QPushButton = QPushButton("Selecionar arquivo")
        self.btn_enviar: QPushButton = QPushButton("Enviar")
        self.btn_enviar.hide()

        layout.addWidget(legenda_arquivos)
        layout.addWidget(self.cbx_zip)
        layout.addWidget(self.cbx_xml)
        layout.addWidget(self.btn_selecionar_arquivo)
        layout.addWidget(self.btn_enviar)

        self.setLayout(layout)

    def __signal(self):
        self.cbx_xml.toggled.connect(lambda: self.__toggleState(self.cbx_xml, self.cbx_xml.checkState()))
        self.cbx_zip.toggled.connect(lambda: self.__toggleState(self.cbx_zip, self.cbx_zip.checkState()))
        self.btn_selecionar_arquivo.clicked.connect(self.__openFile)
        self.btn_enviar.clicked.connect(self.__sendButton)

    def __toggleState(self, checkbox:QCheckBox, state:Qt.CheckState):

        if checkbox == self.cbx_xml and state == Qt.CheckState.Checked:
            self.cbx_zip.setCheckState(Qt.CheckState.Unchecked)
            self.__selectedTypeFile = ".xml"

        if checkbox == self.cbx_zip and state == Qt.CheckState.Checked:
            self.cbx_xml.setCheckState(Qt.CheckState.Unchecked)
            self.__selectedTypeFile = ".zip"

    def __openFile(self):
        dialog: QFileDialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)

        filepath: Path = Path(dialog.getOpenFileName()[0])
        filetype: str = filepath.suffix

        if not filetype == self.__selectedTypeFile:
            msg: QMessageBox = QMessageBox(QMessageBox.Warning,\
                                            'Arquivo inválido',\
                                            'Arquivo selecionado não é válido!'
                                            )
            return msg.exec()

        self.__selectedFile = File(filepath)
        self.btn_enviar.show()

    def __sendButton(self):
        data = self.__selectedFile.data
        Sheets(data)
        QMessageBox(QMessageBox.Information, 'Arquivo salvo', 'Arquivo salvo na aréa de trabalho!').exec()
        
            
    

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        
        content: QWidget = UserInterface()
        
        #window config
        self.setWindowTitle('Conversor de xml para excel')  
        self.setCentralWidget(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())