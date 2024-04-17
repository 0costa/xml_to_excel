from pathlib import Path
from zipfile import ZipFile
import os, shutil
from ..entities.fileXml import Xml

class File:
    def __init__(self, filepath:Path):
        self.__path: Path = filepath
        self.__tempFolder: str = os.path.join(os.environ['USERPROFILE'], 'desktop', 'tempXml')
        self.__dataFile: list = []

        # Remove tempFolder from desktop
        shutil.rmtree(self.__tempFolder, ignore_errors=True)
        
        if self.__path.suffix == '.zip':
            self.__unzip()
            self.__read()
    
    def __str__(self):
        return str(self.__path)
    
    def __unzip(self):
        with ZipFile(self.__path) as myzip:
            myzip.extractall(self.__tempFolder)

    def __read(self):
        for file in os.listdir(self.__tempFolder):
            file = Xml(os.path.join(self.__tempFolder, file))
            file = file.fomartedData

            self.__dataFile.append(file)

    @property
    def data(self):
        shutil.rmtree(self.__tempFolder, ignore_errors=True)
        os.remove(self.__path)
        return self.__dataFile