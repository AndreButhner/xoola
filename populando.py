#!/usr/bin/python3
from app import db
from app.model import Categoria, Movimentacao, Docs, Usuario, Empresa, Formapagamento
import datetime



forma = Formapagamento("DINHEIRO")
forma.add(forma)

forma = Formapagamento("CARTÃO")
forma.add(forma)

forma = Formapagamento("CHEQUE")
forma.add(forma)



#mov = Movimentacao("Luz","conta do mes",100, datetime.date(2015, 10, 12), 1, 1)
#mov.add(mov)

emp = Empresa('XOOLA','trigo@localhost','clodonil','clodonil')
emp.add(emp)

user = Usuario('admin','admin','admin@localhost','admin','x',1)
user.add(user)
