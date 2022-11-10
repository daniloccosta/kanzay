#consulta produto
db_name = "postgres"
db_schema = "kanzay"

sqlAllProd = f"select id from {db_schema}.produtos"

sqlCProd = f"insert into {db_schema}.produtos " + "values({},'{}')"

sqlCNota = f"insert into {db_schema}.pedidos"
sqlCNota += """
(dt_emissao,id_origem,num_nota,num_pedido,valor_desconto,valor_nota)
 values('{}',{},{},{},{},{})
"""

# sqlIdPedido = f"select id from {db_schema}.pedidos "
sqlIdPedido = f"select max(id) from {db_schema}.pedidos "
# sqlIdPedido += "where num_nota={} and id_origem=1"

sqlCFPag = f"insert into {db_schema}.fpag_pedidos(id_pedido,id_forma_pagto,valor) " + "values({},{},{})"

sqlCItem = f"insert into {db_schema}.itens_pedidos(id_pedido,id_produto,quantidade,valor_unit,valor_desc) " + "values({},{},{},{},{})"