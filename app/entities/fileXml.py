import xml.etree.ElementTree as ET, datetime

class Xml:
    def __init__(self, file) -> None:
        self.__tree = ET.parse(file)
        self.__document: dict = {
            'loja': '',
            'cnpjLoja': '',
            'numNfe': '',
            'fornecedor': '',
            'cfop': '',
            'itens': '',
            'valor': '',
            'emissao': '',
            'infoComplementar':''
        }

        self.__read()
    def __read(self) -> list:
        uri: str = '{http://www.portalfiscal.inf.br/nfe}'
        root = self.__tree.getroot()

        nfe = root.find(uri+'NFe')
        infonfe = nfe.find(uri+'infNFe')
        dadosNFe = self.__getDadosNfe(uri, infonfe.find(uri+'ide'))
        dadosEmitente = self.__getEmitente(uri, infonfe.find(uri+'emit'))
        dadosDestinatario = self.__getDestinatario(uri, infonfe.find(uri+'dest'))
        produtos = self.__getDadosProduto(uri, infonfe.findall(uri+'det'))
        total = self.__getTotal(uri, infonfe.find(uri+'total').find(uri+'ICMSTot'))
        informacaoComplementar = self.__getInfComplementar(uri, infonfe.find(uri+'infAdic'))

        for i in (dadosNFe, dadosEmitente, dadosDestinatario, produtos, total, informacaoComplementar):
            if not i:
                continue
             
            self.__document.update(i)

    def __getDadosNfe(self, uri, el):
        try:
            numeroNfe: int = int(el.find(uri+'nNF').text)
            stringDate: str = el.find(uri+'dhEmi').text.split('T')[0]

            stringDate= str(datetime.datetime.strptime(stringDate, '%Y-%m-%d').strftime('%d/%m/%Y'))
            dataEmissao = datetime.datetime.strptime(stringDate, '%d/%m/%Y')

            return {'numNfe': numeroNfe, 'emissao': dataEmissao}        
        except:
            return
        
    def __getEmitente(self, uri, el):
        try:
            loja: int = int(el.find(uri+'xFant').text.split('-')[0])
            cnpjLoja: str = el.find(uri+'CNPJ').text

            return {'loja': loja, 'cnpjLoja': cnpjLoja}
        except:
            return

    def __getDestinatario(self, uri, el)-> dict:
        try:
            fornecedor: str = el.find(uri+'xNome').text

            return {'fornecedor': fornecedor}
        except:
            return

    def __getDadosProduto(self, uri, el)-> dict:
        try:
            itens: int = 0
            cfop: int  = 0

            for i in el:
                prod = i.find(uri+'prod')

                cfop = int(prod.find(uri+'CFOP').text)
                itens += int(prod.find(uri+'qCom').text.split('.')[0])

            return {'itens': itens, 'cfop': cfop}
        except:
            return
            
    def __getTotal(self, uri, el)-> dict:
        try:
            valor: float = float(el.find(uri+'vNF').text)

            return {'valor': valor}
        except:
            return

    def __getInfComplementar(self, uri, el)-> dict:
        try:
            infComplementar: str = el.find(uri+'infCpl').text

            return {'infoComplementar': infComplementar}
        except:
            return

    @property
    def fomartedData(self):
        return self.__document
    
