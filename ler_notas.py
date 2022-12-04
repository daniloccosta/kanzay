import os
import xml.etree.ElementTree as ET
from xmlrpc.client import Boolean
from tkinter import filedialog
from tkinter import *
from pathlib import Path
from datetime import datetime

from banco import Banco

DEBUG = True
NoneType = type(None)
dt_format = "yyyy-MM-ddTHH:mm:ssSXXX"

def obter_arquivos_xml( diretorio ):
    ret = []
    for arq in os.listdir( diretorio ):
        if arq.endswith(".xml"):
            ret.append( os.path.join( diretorio, arq ) )
    return ret

def gravarNotasFiscais(xml):
    nsNFe = { "ns" : "http://www.portalfiscal.inf.br/nfe" }
    root = ET.parse(xml).getroot()
    #Numero Nota Fiscal
    strns = "./ns:NFe/ns:infNFe/ns:ide/ns:nNF"
    node_pg = root.findall( strns, nsNFe )
    num_nota = node_pg[0].text if( node_pg != NoneType and len(node_pg) > 0) else 0

    #Numero Nota Fiscal
    strns = "./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi"
    node_pg = root.findall( strns, nsNFe )
    now = datetime.now()
    dt_emissao = datetime.fromisoformat(node_pg[0].text) if( node_pg != NoneType and len(node_pg) > 0) else NoneType
    

    #Valor total Nota Fiscal
    #strns = "./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF"
    strns = "./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot"
    node_pg = root.findall( strns, nsNFe )
    valor_nota = node_pg[0][8].text if( node_pg != NoneType and len(node_pg) > 0) else 0
    valor_desc = float(node_pg[0][11].text) if( node_pg != NoneType and len(node_pg) > 0) else 0

    #Forma e valor de pagamento
    strns = "./ns:NFe/ns:infNFe/ns:pag/ns:detPag"
    node_pg = root.findall( strns, nsNFe )
    fpags = []
    for detpagto in node_pg:
        fpags.append(tuple([int(detpagto[1].text), float(detpagto[2].text)])) 

    #Itens da nota
    strns = "./ns:NFe/ns:infNFe/ns:det/ns:prod"
    node_pg = root.findall( strns, nsNFe )
    itens = []
    for item in node_pg:
        id   = int(item[0].text)
        prod = item[2].text
        qtde = float(item[6].text)
        vlr  = float(item[7].text)
        desc = float(0)
        itens.append([
            id,         #codigo produto
            prod,       #descricao
            qtde,       #quant
            vlr,        #valor
            desc        #desconto
        ])
    
    if (int(num_nota) >= 0 and dt_emissao != NoneType):
        try:
            if DEBUG:
                print(f"Nota Fiscal: {num_nota}")
            produtos = bd.getProdutos()
            bd.gravarProduto(produtos, itens)
            bd.gravarPedido(dt_emissao, 1, num_nota, 0, valor_desc, valor_nota)
            id_ped = bd.getIdPedido()
            if fpags != None:
                bd.gravarFormaPagto(id_ped, fpags)
            bd.gravarItens(id_ped, itens)
            # listarProdutos() #atualizar lista de produtos
        except Exception as e:
            print("Error:", e)

def selectRootDir():
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory()

def lerArquivosXML():
    rootDirXML = selectRootDir()
    if rootDirXML == "":
        raise Exception("O local dos arquivos deve ser selecionado") 

    arquivos = Path(rootDirXML).glob('**/*.xml')
    for arquivo in arquivos:
        gravarNotasFiscais(arquivo)
    
    #for nota in notas:
    #    listar_notas_canceladas(nota)
    
    #for nota in notas:
    #    gravarNotasFiscais(nota)

if __name__ == '__main__':
    bd = Banco()
    # listarProdutos()
    print("Iniciando leitura dos arquivos xml..")
    lerArquivosXML()
    print("Processo concluido")
    bd.fechar()