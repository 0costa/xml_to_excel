from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget, QCheckBox, QLabel, QPushButton, QFileDialog, QMessageBox
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtGui import Qt
from pathlib import Path
from .entities.file import File
from .entities.sheets import Sheets

class UserInterface(QWidget):
    def __init__(self) -> QWidget:
        super().__init__()

        self.__selectedFile: File;

        self.__ui()
        self.__signal()

    def __ui(self):
        layout: QVBoxLayout = QVBoxLayout()
        self.legenda_arquivos: QLabel = QLabel("Arquivos selecionados\n\n")

        self.btn_selecionar_arquivo: QPushButton = QPushButton("Selecionar arquivo")
        self.btn_enviar: QPushButton = QPushButton("Enviar")
        self.btn_enviar.hide()

        layout.addWidget(self.legenda_arquivos)
        layout.addWidget(self.btn_selecionar_arquivo)
        layout.addWidget(self.btn_enviar)

        self.setLayout(layout)

    def __signal(self):
        self.btn_selecionar_arquivo.clicked.connect(self.__openFile)
        self.btn_enviar.clicked.connect(self.__sendButton)

    def __openFile(self):
        dialog: QFileDialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)


        filepath: list = dialog.getOpenFileNames()[0]
        filepath = [Path(i) for i in filepath if Path(i).suffix == '.zip']

        if not filepath:
            msgBox = QMessageBox(QMessageBox.Warning, 'Arquivo', 'Nenhum arquivo zip selecionado!')
            return msgBox.exec()

        self.__selectedFile = File(filepath)
        self.btn_enviar.show()

        for x in filepath:
            text = Path(x).stem + '\n'
            new_label = self.legenda_arquivos.text()
            self.legenda_arquivos.setText(new_label + text)

    def __sendButton(self):
        data = self.__selectedFile.data
        Sheets(data)
        QMessageBox(QMessageBox.Information, 'Arquivo salvo', 'Arquivo salvo na aréa de trabalho!').exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        content: QWidget = UserInterface()
        
        #window config
        self.setWindowTitle('Conversor de xml para excel')  
        self.setCentralWidget(content)