from tkinter import filedialog
import tkinter as tk
import pandas as pd

from banco import Banco
import query

DEBUG = True
NoneType = type(None)
dt_format = "yyyy-MM-ddTHH:mm:ssSXXX"

def pedidosCancelados(df: pd.DataFrame):
    return df[(df['TIPO DE LANÇAMENTO'] != 'Pedido')].filter(items=['N° PEDIDO']).groupby(by=['N° PEDIDO']).count()
    
def tratarPlanilha(ifoodfile):
    df = pd.read_excel(ifoodfile, header=0)
    # cols = df.shape[1]
    #for idx, row in df.iterrows():
    #    msg = ""
    #    for i in range(len(df.columns)):
    #        msg += ","+ str(row[df.columns[i]])
    #    if idx == 10:
    #        break
    return df

def gravarPedidosIfood(df: pd.DataFrame):
    cancelados = pedidosCancelados(df)

    #verifica se o pedido está na lista dos cancelados
    def pedidoCancelado(num_ped):
        _max = cancelados.shape[0]
        pcanc = False
        for i in range(_max):
            pcanc = (num_ped == cancelados.iloc[i].name)
            if pcanc: break
        return pcanc
    
    for i in range(len(df)):
        num_ped = df.loc[i, 'N° PEDIDO'] #
        if not pedidoCancelado(num_ped):
            dt_emissao      = df.loc[i, 'DATA']
            id_orig_venda   = 2 #ifood        
            num_nota        = 0
            vr_nota         = df.loc[i, 'TOTAL DO PEDIDO']
            vr_desc         = vr_nota - df.loc[i, 'VALOR LIQUIDO']
            id_fpagto       = 99 #outros
            bd.gravarPedido(dt_emissao, id_orig_venda, num_nota, num_ped, vr_desc, vr_nota)
            id_ped = bd.getIdPedido()
            fpags = []
            fpags.append(tuple([id_fpagto, vr_nota - vr_desc]))
            bd.gravarFormaPagto(id_ped, fpags)

def openExcelFile():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
                filetypes=[
                    ("Excel 2007-365", "*.xlsx"),
                    ("Excel 97-2003", "*.xls")
                ]
            )

def lerPlanilha():
    ifoodfile = openExcelFile()
    if ifoodfile == "":
        raise Exception("A planilha contendo os dados de importação deve ser selecionada") 

    df = tratarPlanilha(ifoodfile)
    gravarPedidosIfood(df)


if __name__ == '__main__':
    bd = Banco()
    lerPlanilha()
    print("Processo concluido")
    bd.fechar()