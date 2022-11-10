import os
from platform import node
import xml.etree.ElementTree as ET
import plotly.express as px
import pandas as pd

#twilio: 9634d3th3neamsnT

NoneType = type(None)
recebmtos = {}
notas_canceladas = []
formas_pgtos = {
    '01': "Dinheiro", 
    '02': "Cheque", 
    '03': "Cartão de Crédito",
    '04': "Cartão de Débito",
    '05': "Crédito Loja",
    '10': "Vale Alimentação",
    '11': "Vale Refeição",
    '12': "Vale Presente",
    '13': "Vale Combustível",
    '14': "Duplicata Mercantil",
    '15': "Boleto Bancário",
    '16': "Depósito Bancário",
    '17': "Pagamento Instantâneo (PIX)",
    '18': "Transferência bancária, Carteira Digital",
    '19': "Programa de fidelidade, Cashback, Crédito Virtual",
    '90': "Sem Pagamento",
    '99': "Outros"
}

def obter_arquivos_xml( diretorio ):
    ret = []
    for arq in os.listdir( diretorio ):
        if arq.endswith(".xml"):
            ret.append( os.path.join( diretorio, arq ) )
    return ret

def totalizar_valor_pago( arquivoNFe ):
    nsNFe = { "ns" : "http://www.portalfiscal.inf.br/nfe" }
    root = ET.parse( arquivoNFe ).getroot()
    strns = "./ns:NFe/ns:infNFe/ns:pag/ns:detPag"
    node_pg = root.findall( strns, nsNFe )
    
    global recebmtos
    
    if( node_pg != NoneType and len(node_pg) > 0):
        for detpagto in node_pg:
            forma = formas_pgtos[detpagto[1].text]
            
            if (forma in recebmtos.keys()):
                recebmtos[forma] += float(detpagto[2].text)
            else:
                recebmtos[forma] = float(detpagto[2].text)
        
    #return recebmtos

def listar_notas_canceladas( arquivoNFe ):
    nsNFe = { "ns" : "http://www.portalfiscal.inf.br/nfe" }
    root = ET.parse( arquivoNFe ).getroot()
    strns = "./ns:NFe/ns:infNFe/ns:ide/ns:nNF"
    node_pg = root.findall( strns, nsNFe )
    
    if( node_pg != NoneType and len(node_pg) > 0):
        #print(node_pg[0].text)
        pass
    else:
        strns = "./ns:evento/ns:infEvento"
        node_pg = root.findall( strns, nsNFe )
        if node_pg != []:
            #print(node_pg[0][3].text[30:35])
            print(node_pg)

def gravarProduto(itens):
    pass

def gravarNota(nota, dt, vr, desc):
    pass

def gravaFormaPagto(fpags):
    pass

def gravarItens(itens):
    pass

def lerXML(xml):
    nsNFe = { "ns" : "http://www.portalfiscal.inf.br/nfe" }
    root = ET.parse(xml).getroot()
    #Numero Nota Fiscal
    strns = "./ns:NFe/ns:infNFe/ns:ide/ns:nNF"
    node_pg = root.findall( strns, nsNFe )
    num_nota = node_pg[0].text if( node_pg != NoneType and len(node_pg) > 0) else 0

    #Numero Nota Fiscal
    strns = "./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi"
    node_pg = root.findall( strns, nsNFe )
    dt_emissao = node_pg[0].text if( node_pg != NoneType and len(node_pg) > 0) else NoneType

    #Valor total Nota Fiscal
    #strns = "./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF"
    strns = "./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot"
    node_pg = root.findall( strns, nsNFe )
    valor_nota = node_pg[0][0].text if( node_pg != NoneType and len(node_pg) > 0) else 0
    vdesc = float(node_pg[0][11].text) if( node_pg != NoneType and len(node_pg) > 0) else 0

    #Forma e valor de pagamento
    strns = "./ns:NFe/ns:infNFe/ns:pag/ns:detPag"
    node_pg = root.findall( strns, nsNFe )
    fpags = []
    for detpagto in node_pg:
        fpags.append(tuple([detpagto[1].text, float(detpagto[2].text)])) 

    #Itens da nota
    strns = "./ns:NFe/ns:infNFe/ns:det"
    node_pg = root.findall( strns, nsNFe )
    itens = []
    for item in node_pg:
        id   = int(item.find('vcod').text) if item.find('vcod') != None else 0
        prod = item.find('xprod').text if item.find('xprod') != None else ''
        qtde = float(item.find('qCom').text) if item.find('qCom') != None else 0.0
        vlr  = float(item.find('vUnCom').text) if item.find('vUnCom') != None else 0.0
        desc = float(item.find('vDesc').text) if item.find('vDesc') != None else 0.0
        itens.append([
            num_nota,   #numero nota
            id,         #codigo
            prod,       #descricao
            qtde,       #quant
            vlr,        #valor
            desc        #desconto
        ])
        
    gravarProduto(itens)
    gravarNota(num_nota, dt_emissao, valor_nota, vdesc)
    gravaFormaPagto(fpags)
    gravarItens(itens)


def ler_notas():
    notas = obter_arquivos_xml("src/xml/092022/")
    
    #for nota in notas:
    #    listar_notas_canceladas(nota)
    
    for nota in notas:
        #totalizar_valor_pago(nota)
        lerXML(nota)
    
def plotarGrafico():
    df = pd.DataFrame(recebmtos.items(), columns=['Forma Pagto', 'Valor Recebido'])
    tt = df['Valor Recebido'].sum()
    
    #fig = px.pie(
    #        df, 
    #        values     = 'Valor Recebido', 
    #        names      = 'Forma Pagto', 
    #        hole       = .3,
    #        title      = 'R$ {:.2f}'.format(tt)
    #    )

    fig = px.bar(
        df, x='Valor Recebido', y='Forma Pagto',
        title='Total R$ {:.2f}'.format(tt),
        text_auto='.2f'
    )
    #fig.show()
    fig.write_image('graph1.png')

if __name__ == '__main__':
    ler_notas()
    #plotarGrafico()