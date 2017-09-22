	#!env/bin/python
from app import db
from app.model import Categoria, Movimentacao, Docs, Usuario, Empresa, Formapagamento
import datetime
from dateutil.relativedelta import relativedelta


movs = Movimentacao.query.filter(Movimentacao.parcelas == 5000).all()

for mov in movs:
    movs_parcela = Movimentacao.query.filter(Movimentacao.parcelas_id == mov.parcelas_id, Movimentacao.id >= mov.id).all()
    print(mov.parcelas)
    for nparcela in movs_parcela:
        #nparcela.delete(nparcela)    
        print(nparcela.id, nparcela.parcelas, nparcela.parcelas_id)
	

	
