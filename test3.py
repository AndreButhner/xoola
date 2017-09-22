from app import db
from app.model import Categoria, Movimentacao, Docs, Usuario, Empresa, Formapagamento
from dateutil.relativedelta import relativedelta
from celery.task import task
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

head = "<style type='text/css'>.tg{border-collapse:collapse;border-spacing:0;border-color:#ccc;}.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;}.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f0f0f0;}.tg .tg-3fff{font-weight:bold;color:#330001;text-align:center;vertical-align:top}.tg .tg-jo0b{background-color:#f9f9f9;font-weight:bold;vertical-align:top}.tg .tg-i6eq{background-color:#ffccc9;vertical-align:top}.tg .tg-c3cn{background-color:#ffccc9;text-align:right;vertical-align:top}.tg .tg-pgb8{background-color:#ffcc67;vertical-align:top}.tg .tg-yw4l{vertical-align:top}.tg .tg-lqy6{text-align:right;vertical-align:top}.tg .tg-6kxl{background-color:#f0f0f0;font-weight:bold;text-align:right;vertical-align:top}.tg .tg-lhw2{background-color:#f0f0f0;text-align:right;vertical-align:top}.tg .tg-p5oz{background-color:#f9f9f9;text-align:right;vertical-align:top}</style><table class='tg'> <tr> <th class='tg-3fff' colspan='4'>Contas a Pagar<br></th> </tr><tr> <td class='tg-jo0b'>No</td><td class='tg-jo0b'>Data</td><td class='tg-jo0b'>Descri&ccedil;&atilde;o<br></td><td class='tg-jo0b'>Valor<br></td></tr>"

hoje   = date.today()

emps = Empresa.query.all()

# Varrendo todas as contas
for emp in emps:
    pags = Movimentacao.query.join(Categoria, Movimentacao.categoria_id == Categoria.id).filter(Categoria.status == 1,Movimentacao.efetuado == None, Movimentacao.empresa_id == emp.id ).order_by('data_v').all()
    #recs = Movimentacao.query.join(Categoria, Movimentacao.categoria_id == Categoria.id).filter(Categoria.status == 0,Movimentacao.efetuado == None, Movimentacao.empresa_id == session['empresa'] ).order_by('data_v').all()


    psoma  = sum([item.valor  for item in pags])
    pvencida = []
    pdia     = []
    pamanha  = []

    for pag in pags:
         if pag.data_v < hoje:
            pvencida.append(pag)
         elif pag.data_v == hoje:
            pdia.append(pag)
         elif pag.data_v == hoje + timedelta(days=3):
            pamanha.append(pag)

    phtml = dhtml = ahtml = ""

    id = 1          
    for mov in pvencida:      
      phtml = phtml + "<tr> <td class='tg-i6eq'>{}</td><td class='tg-i6eq'>{}</td><td class='tg-c3cn'>{}</td><td class='tg-c3cn'>{}</td></tr>".format(id,mov.data_v.strftime('%d/%m/%Y'),mov.titulo,mov.valor)
      id = id + 1

    for mov in pdia:
       dhtml = dhtml + "<tr> <td class='tg-pgb8'>{}</td><td class='tg-pgb8'>{}</td><td class='tg-pgb8'>{}</td><td class='tg-pgb8'>{}</td></tr>".format(id,mov.data_v.strftime('%d/%m/%Y'),mov.titulo,mov.valor)
       id = id + 1

    for mov in pamanha:
       ahtml = ahtml + "<tr> <td class='tg-yw4l'>{}</td><td class='tg-yw4l'>{}</td><td class='tg-lqy6'>{}</td><td class='tg-lqy6'>{}</td></tr>".format(id,mov.data_v.strftime('%d/%m/%Y'),mov.titulo,mov.valor)
       id = id + 1


    
    html = head + phtml + dhtml + ahtml + "<tr><td class='tg-6kxl' colspan='3'>Total</td><td class='tg-p5oz'>{}</td></tr></table>".format(psoma)               

          
        
    send_mail('[FINACEIRO]: Fluxo de Pagamento', 'clodonil@decoroecsa.com.br', sender,'teste',html)

    
#send_mail('Teste de envio de email do python', 'clodonil@decoroecsa.com.br',['clodonil@nisled.org'],'teste','<h1> teste </h1>')

