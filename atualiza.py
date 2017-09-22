#!env/bin/python
from app import db
from app.model import Movimentacao
import datetime
from dateutil.relativedelta import relativedelta

hoje = datetime.date.today()

# Contas Fixas
#fixa = Movimentacao.query.filter(Movimentacao.parcelas == 0).all()
#for registro in fixa:
#    if registro.data_v < hoje:
#       p_data = registro.data_v + relativedelta(months=+1)
#       mov = Movimentacao(
#                          registro.titulo, 
#                          registro.descricao, 
#                          registro.valor, 
#                          p_data,
#                          registro.parcelas, 
#                          registro.categoria_id,
#                          registro.formapagamento_id
#                         )
#       mov.parcela_id = registro.parcelas_id
#       mov.usuario_id = registro.usuario_id
#       print(mov.add(mov))


# Parcelas
parcelas = Movimentacao.query.filter(Movimentacao.parcelas > 0).all()
for registro in parcelas:
    print(registro.titulo)
