from openpyxl import Workbook
import os
from datetime import datetime

class Sheets():
    WB = Workbook()
    SHEET = WB.active
   
    def __init__(self, data):
        fieldnames = ['loja','cnpjLoja','numNfe','fornecedor','cfop','itens','valor','emissao','infoComplementar']

        self.SHEET.append(['Loja', 'CNPJ', 'Num. NFe', 'Fornecedor', 'Cfop', 'Itens', 'Valor', 'Emissão', 'Informação complementar'])
        for nf in data:
            values = (nf[k] for k in fieldnames)
            self.SHEET.append(values)

        actualDate = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        sheetname = f'Notas_fiscais_{actualDate}.xlsx'
        destino = os.path.join(os.environ['USERPROFILE'], 'desktop', sheetname)
        self.WB.save(destino)