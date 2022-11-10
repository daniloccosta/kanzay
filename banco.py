import os
import psycopg2 as pg
from psycopg2.extensions import make_dsn
from datetime import datetime
import base64
import query

class Banco(object):
    _db = None
    DEBUG = True

    def abracadabra(self, value: str):
        b64b = value.encode('ascii')
        msgb = base64.b64decode(b64b)
        return msgb.decode('ascii').replace("\n", "")

    def __init__(self):
        db_name = self.abracadabra("cG9zdGdyZXMK")
        db_user = self.abracadabra("cG9zdGdyZXMK")
        db_pass = self.abracadabra("Mjc1MjY1Cg==")
        db_port = self.abracadabra("NTQzMgo=")
        dsn = make_dsn(f"dbname='{db_name}' user='{db_user}' password='{db_pass}' host='localhost' port={db_port}")
        self._db = pg.connect(dsn)

    def manipular(self, sql):
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print("Error:", e)
            print(sql)
            return False
        return True

    def consultar(self, sql):
        rs = None
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            rs = cur.fetchall()
            cur.close()
        except Exception as e:
            print("Error:", e)
            return None
        return rs

    def fechar(self):
        self._db.close()

    def gravarPedido(self, 
        dt_emissao: datetime,
        id_origem: int,
        num_nota: int,
        num_pedido: int, 
        vr_desconto: float, 
        vr_nota: float):
    
        if self.DEBUG:
            print(f"  Gravando NF..")

        self.manipular(
            query.sqlCNota.format(
                dt_emissao, 
                id_origem,
                num_nota,
                num_pedido,
                vr_desconto, 
                vr_nota
            )
        )

    def getProdutos(self):
        return self.consultar(query.sqlAllProd)

    def produtoCadastrado(self, produtos: list, produto: int):
        for prod in produtos:
            if int(prod[0]) == produto:
                return True

        return False

    def gravarProduto(self, produtos: list, itens):
        if self.DEBUG:
            print(f"  Verificando cadastro de produtos..")

        for item in itens:
            if self.produtoCadastrado(produtos, item[0]) == False:
                self.manipular(query.sqlCProd.format(item[0], item[1]))
    
    def gravarFormaPagto(self, id_pedido, fpags):
        if self.DEBUG:
            print(f"  Gravando pagamentos da NF..")
        for fpag in fpags:
            cmd = query.sqlCFPag.format(id_pedido, fpag[0], fpag[1])
            self.manipular(cmd)

    def gravarItens(self, id: int, itens: list):
        if self.DEBUG:
            print(f"  Gravando itens da NF..")

        for item in itens:
            self.manipular(query.sqlCItem.format(
                str(id),
                item[0],
                item[2],
                item[3],
                item[4]))
    
    def getIdPedido(self) -> int:
        # return self.consultar(query.sqlIdPedido.format(num_nota))
        return self.consultar(query.sqlIdPedido)[0][0]