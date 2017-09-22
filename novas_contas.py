#!/opt/flask/Projetos/xoolo/env/bin/python
from app import db
from app.model import Categoria, Movimentacao, Docs, Usuario, Empresa, Formapagamento
import datetime
from dateutil.relativedelta import relativedelta


hoje = datetime.date.today()

def criar_registro(registro):
  p_data = registro.data_v + relativedelta(months=+1)
  mov = Movimentacao(
                          registro.titulo,
                          registro.descricao,
                          registro.valor,
                          p_data,
                          registro.parcelas,
                          registro.categoria_id,
                          registro.formapagamento_id,
                          registro.conta_id
                         )

  mov.parcelas_id = registro.parcelas_id
  mov.empresa_id = registro.empresa_id
  mov.add(mov)



def contas_parceladas():
   # pesquisa todas as contas parceladas
   movs =  Movimentacao.query.filter(Movimentacao.parcelas > 1, Movimentacao.finalizada == False ).order_by('data_v').all()
   lista_parcelas = []
   for mov in movs:
       if not mov.parcelas_id in lista_parcelas:
          index = 0
          lista_parcelas.append(mov.parcelas_id)
          for item in movs:
              if mov.parcelas_id == item.parcelas_id:
                 ultimo = index
              index=index+1
          
          if movs[ultimo].data_v.month < hoje.month and index < mov.parcelas:
             print("Conta parcelada criada")
             criar_registro(movs[ultimo])

def finalizar_contas():

  ''' 
       Contas Parcelas
  '''
  movs =  Movimentacao.query.filter(Movimentacao.parcelas > 1, Movimentacao.finalizada == False ).all()
  for mov in movs:
      if len(Movimentacao.query.filter(Movimentacao.parcelas_id == mov.parcelas_id).all()) >= mov.parcelas:
          mov.finalizada = True
          mov.update()

  '''
   Contas fixas
  '''   
  movs = Movimentacao.query.filter(Movimentacao.parcelas == 1000, Movimentacao.finalizada == False ).all()
  for mov in movs:      
      for item in Movimentacao.query.filter(Movimentacao.parcelas_id == mov.parcelas_id).all():          
          item.finalizada = True
          item.update()
  


def contas_fixas():
   # pesquisa todas as contas fixas
   movs =  Movimentacao.query.filter(Movimentacao.parcelas == 0, Movimentacao.finalizada == False ).order_by('data_v').all()
   lista_parcelas = []
   for mov in movs:
       if not mov.parcelas_id in lista_parcelas:
          index = 0
          lista_parcelas.append(mov.parcelas_id)
          for item in movs:
              if mov.parcelas_id == item.parcelas_id:
                 ultimo = index
              index=index+1

          if movs[ultimo].data_v.month < hoje.month:
             print("Conta parcelada criada")
             criar_registro(movs[ultimo])


finalizar_contas()
contas_parceladas()
contas_fixas()


