from pathlib import Path
from zipfile import ZipFile
import os, shutil
from ..entities.fileXml import Xml

class File:
    def __init__(self, list:Path):
        self.__pathlist: Path = list
        self.__tempFolder: str = os.path.join(os.environ['USERPROFILE'], 'desktop', 'tempXml')
        self.__dataFile: list = []

        # Remove tempFolder from desktop
        shutil.rmtree(self.__tempFolder, ignore_errors=True)
        
        self.__unzip()
        self.__read()
    
    def __str__(self):
        return str(self.__path)
    
    def __unzip(self):
        for path in self.__pathlist:
            with ZipFile(path) as myzip:
                myzip.extractall(self.__tempFolder)

    def __read(self):
        for file in os.listdir(self.__tempFolder):
            file = Xml(os.path.join(self.__tempFolder, file))
            file = file.fomartedData

            self.__dataFile.append(file)

    @property
    def data(self):
        shutil.rmtree(self.__tempFolder, ignore_errors=True)

        for path in self.__pathlist:
            os.remove(path)
            
        return self.__dataFile