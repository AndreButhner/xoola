from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from sqlalchemy.sql import func
from werkzeug import secure_filename
from app import app,mail,db, babel
from app.controllers.movimentacao.forms import MovForm, MovRealizadoForm, DocsForm, RelForm, PesqForm
from app.model import Movimentacao,Docs, Categoria,Formapagamento, Usuario, Empresa, Conta
from config import UPLOAD_FOLDER
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from datetime import datetime, timedelta, date
from celery.task import task
from dateutil.relativedelta import relativedelta
import locale



# Staus
# Parcelas: 5000 para cancelar parcelas
# Parcelas: 6000 canceladas apos alteracao
# Parcelas: 7000 Recorrentes já duplicadas
 


## Criar os registros das contas parceladas
@task
def cad_parcelado(mov_id):
    #contas recorrentes
    freq  = {
               1000:1,
               1200:7,
               1300:10,
               1400:15,
               1500:28,
               1600:30,
               1700:60,
               1800:90,
               1900:120,
               2000:181,
               2100: 365 
             } 

    mov    = Movimentacao.query.get(mov_id)


    if not mov.parcelas in freq: 

        #Ultima data
        u_data = mov.data_v 
        for parcela in range(2,mov.parcelas+1):

            # Criando um novo registro
            novo = Movimentacao(
                               mov.titulo,
                               mov.descricao,
                               mov.valor,
                               mov.data_v,
                               parcela,                           
                               mov.categoria_id,                          
                               mov.formapagamento_id,
                               mov.conta_id
                              )       
            

            novo.empresa_id  = mov.empresa_id
            novo.parcelas_id = mov.parcelas_id 
            novo.data_v      = u_data + relativedelta(months=1)             

            novo.add(novo)
            u_data           = novo.data_v
        
        #Atualizando as primeiras parcelas
        mov.parcelas     = 1
        mov.update()       
        return(mov_id)

## Finalizar uma conta fixa ou parcelada
## Se for parceladas, deve excluir as contas já criadas
@task
def finalizar_contas():

     ''' 
       Contas Parcelas
     '''
     ### Parcelas 5000 para cancelar
     ### Parcelas 6000 canceladas


     movs = Movimentacao.query.filter(Movimentacao.parcelas == 5000).all()

     for mov in movs:
         movs_parcela = Movimentacao.query.filter(Movimentacao.parcelas_id == mov.parcelas_id, Movimentacao.id >= mov.id).all()
         for nparcela in movs_parcela:
             nparcela.parcelas   = 6000
             nparcela.finalizada = True
             nparcela.efetuado   = True
             nparcela.update()

     return(True)


# Criar novas contas fixas(recorrentes), no dia do vencimento. 
@task
def contas_fixas():
    # pesquisa todas as contas fixas
    freq  = {
               1000:1,
               1200:7,
               1300:10,
               1400:15,
               1500:28,
               1600:30,
               1700:60,
               1800:90,
               1900:120,
               2000:181,
               2100: 365 
             } 

    # data de hoje
    hoje   = date.today()

    movs =  Movimentacao.query.filter(Movimentacao.parcelas.in_((1000,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100))).order_by('data_v').all()
    for mov in movs:
        # Se a conta foi paga antes ou esta vencida deve ser criada a conta do mes seguinte
        if mov.data_v <= hoje or mov.efetuado == True:
            print(mov.titulo)
            novo = Movimentacao(
                           mov.titulo,
                           mov.descricao,
                           mov.valor,
                           mov.data_v,
                           mov.parcelas,                           
                           mov.categoria_id,                          
                           mov.formapagamento_id,
                           mov.conta_id
                          )       
            novo.empresa_id  = mov.empresa_id
            novo.parcelas_id = mov.parcelas_id 
            novo.data_v      = mov.data_v + relativedelta(days=freq[mov.parcelas])
            novo.add(novo)

            mov.parcelas = 7000
            mov.update()
    return(True)   

def send_mail(subject,  recipients, text_body, html_body):
    sender = 'clodonil@decoroecsa.com.br'
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    with app.app_context():
        mail.send(msg)



def formatar_dinheiro(value):
  if type(value) == str:
      value = int(value)
  locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
  valor = locale.currency(value, grouping=True, symbol=None)
  return "R$ {}".format(valor)

def parcelas(parcelas,parcela_id):

  # Staus
  # Parcelas: 5000 para cancelar parcelas
  # Parcelas: 6000 canceladas apos alteracao
  # Parcelas: 7000 Recorrentes já duplicadas
 
  freq  = {
            1000:'Diário',
            1200:'Semanal',
            1300:'A cada 10 dias',
            1400:'A cada 15 dias',
            1500:'A cada 28 dias',
            1600:'Mensal',
            1700:'Bimestral',
            1800:'Trimestral',
            1900:'Quadrimestral',
            2000:'Semestral',
            2100:'Anual' 
           } 
  nparcela = Movimentacao.query.filter(Movimentacao.parcelas_id==parcela_id).all()

  if parcelas in freq:
      return "Recorrente {}".format(freq[parcelas])
  elif parcelas == 7000:
      return 'Recorrentes'   
  elif len(nparcela) >= 1:
      return "{} de {}".format(parcelas,len(nparcela))


   

           
@task
def ordem_pagamento():
    

    hoje   = date.today()
    emps   = Empresa.query.filter(Empresa.id != 1).all()

    titulo   = "<h1 style='text-align: center;'><u><strong>Fluxo de Pagamentos</strong></u></h1><div style='background:#eee;border:1px solid #ccc;padding:5px 10px;'><span style='font-size:14px;'><strong>Empresa:</strong></span>&nbsp;{}</div><p>&nbsp;</p>"
    phead    = "<table cellspacing='0' cellpadding='0' border='1' bgcolor='#EEEEE0' bordercolor='#CDBE70'><tr><td><table cellspacing='0' cellpadding='2' border='1' bgcolor='#EEEEE0' bordercolor='#FFFFFF'><tr><td colspan='5' align='center'><strong>Contas &agrave; Pagar</strong></td></tr><tr align='center'><td width='5'><strong>N&ordm;</strong></td><td width='30'><strong>Data</strong></td><td width='210'><strong>Lan&ccedil;amento</strong></td><td width='130'><strong>Parcelas</strong></td><td width='90'><strong>Valor</strong></td></tr>"
    rhead    = "<table cellspacing='0' cellpadding='0' border='1' bgcolor='#EEEEE0' bordercolor='#00FA9A'><tr><td><table cellspacing='0' cellpadding='2' border='1' bgcolor='#EEEEE0' bordercolor='#FFFFFF'><tr><td colspan='5' align='center'><strong>Contas &agrave; Receber</strong></td></tr><tr align='center'><td width='5'><strong>N&ordm;</strong></td><td width='30'><strong>Data</strong></td><td width='210'><strong>Lan&ccedil;amento</strong></td><td width='130'><strong>Parcelas</strong></td><td width='90'><strong>Valor</strong></td></tr>"
    vencida  = "<tr bgcolor='#FF4040'><td width='5'>{}</td><td width='30'>{}</td><td width='210'>{}</td><td width='130'>{}</td><td width='90'>{}</td></tr>"
    lhoje    = "<tr bgcolor='#FFD700'><td width='5'>{}</td><td width='30'>{}</td><td width='210'>{}</td><td width='130'>{}</td><td width='90'>{}</td></tr>"
    amanha   = "<tr bgcolor='#E3E3E3'><td width='5'>{}</td><td width='30'>{}</td><td width='210'>{}</td><td width='130'>{}</td><td width='90'>{}</td></tr>"  
    close    = "<tr><td colspan='4' align='right'><strong>Total</strong></td><td>{}</strong></td></tr></table></td></tr></table>"
    rodape   = "<p>&nbsp;</p><p><em style='line-height: 1.6em;'>Clodonil H Trigo</em></p>"

    # Varrendo todas as contas
    for emp in emps:
            pags = Movimentacao.query.join(Categoria, Movimentacao.categoria_id == Categoria.id).filter(Categoria.status == 1,Movimentacao.efetuado == None, Movimentacao.empresa_id == emp.id ).order_by('data_v').all()
            recs = Movimentacao.query.join(Categoria, Movimentacao.categoria_id == Categoria.id).filter(Categoria.status == 0,Movimentacao.efetuado == None, Movimentacao.empresa_id == emp.id ).order_by('data_v').all()

            psoma    = 0

            rsoma    = 0

            pid = 1
            html = titulo.format(emp.nome)

            for pag in pags:
                if pid == 1:
                   html = html + phead

                if pag.data_v < hoje:
                   html = html + vencida.format(pid,pag.data_v.strftime('%d/%m/%Y'),pag.titulo,parcelas(pag.parcelas,pag.parcelas_id),formatar_dinheiro(pag.valor))
                   psoma = psoma + pag.valor

                elif pag.data_v == hoje:
                   html = html + lhoje.format(pid,pag.data_v.strftime('%d/%m/%Y'),pag.titulo,parcelas(pag.parcelas,pag.parcelas_id),formatar_dinheiro(pag.valor))                   
                   psoma = psoma + pag.valor

                elif pag.data_v > hoje and pag.data_v <= hoje + timedelta(days=30):
                   psoma = psoma + pag.valor
                   html = html + amanha.format(pid,pag.data_v.strftime('%d/%m/%Y'),pag.titulo,parcelas(pag.parcelas,pag.parcelas_id),formatar_dinheiro(pag.valor))
                pid = pid + 1
            html = html + close.format(formatar_dinheiro(psoma)) + "<br/><br/><br/>"       
            
            id = 1
            for rec in recs:
                if id == 1:
                   html = html + rhead

                if rec.data_v < hoje:                   
                   rsoma = rsoma + rec.valor
                   html = html + vencida.format(id,rec.data_v.strftime('%d/%m/%Y'),rec.titulo,parcelas(rec.parcelas,rec.parcelas_id),formatar_dinheiro(rec.valor))
                elif rec.data_v == hoje:
                   html = html + lhoje.format(id,rec.data_v.strftime('%d/%m/%Y'),rec.titulo,parcelas(rec.parcelas,rec.parcelas_id),formatar_dinheiro(rec.valor))
                   rsoma = rsoma + rec.valor
                elif rec.data_v > hoje and rec.data_v <= hoje + timedelta(days=30):
                   rsoma = rsoma + rec.valor
                   html = html + amanha.format(id,rec.data_v.strftime('%d/%m/%Y'),rec.titulo,parcelas(rec.parcelas,rec.parcelas_id),formatar_dinheiro(rec.valor))
                id = id + 1
            html = html + close.format(formatar_dinheiro(rsoma))    
            html = html + rodape   

            # Envia o email
            titulo = "[ {} ]: Fluxo de Pagamento".format(emp.nome.upper())
            #send_mail('[MEDPARC]: Fluxo de Pagamento', [user.email for user in emp.Usuario.all()],'Fluxo de Pagamento',html)
            print(html)




