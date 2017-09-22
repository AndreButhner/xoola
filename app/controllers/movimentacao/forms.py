from flask_wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField,validators
from wtforms.validators import DataRequired
from app.model import Categoria,Formapagamento
from datetime import datetime

class MovForm(Form):


     freq  = [
               (1,'Uma única vez'),
               (1000,'Diariamente'),
               (1200,'Semanal'),
               (1300,'A cada 10 dias'),
               (1400,'A cada 15 dias'),
               (1500,'A cada 28 dias'),
               (1600,'Mensal'),
               (1700,'Bimestral'),
               (1800,'Trimestral'),
               (1900,'Quadrimestral'),
               (2000,'Semestral'),
               (2100, 'Anual') 
             ] 


#     nparcelas = []
#     nparcelas.append((0,'Conta Fixa'))
#     nparcelas.append((1000,'Finalizar - Conta Fixa'))
     for a in range(2,500):
        freq.append((a,'%d-Parcelas' %a))

     #Contas Canceladas
     freq.append((5000,'Cancelamento'))   


     titulo       = StringField('titulo', validators=[DataRequired()])
     descricao    = TextAreaField('titulo', validators=[DataRequired()])
     valor        = FloatField('valor', validators=[DataRequired()])
     parcelas     = SelectField('parcelas', choices=freq,coerce=int)
     data_v       = DateField("Until", format="%d/%m/%Y",default=datetime.today, validators=[validators.DataRequired()])
     categoria_id = SelectField('categorias',coerce=int)
     conta_id     = SelectField('Conta',coerce=int)

     formapagamento_id = SelectField('formapagamento', coerce=int)



class MovRealizadoForm(Form):
     valor           = FloatField('valor', validators=[DataRequired()])
     juros           = FloatField('juros', default=0.0)
     multa           = FloatField('multa', default=0.0)
     desconto        = FloatField('desconto', default=0.0)
     data_pagamento  = DateField("Pagamento", format="%d/%m/%Y",default=datetime.today, validators=[validators.DataRequired()])
     comprovante     =  FileField('comprovante')

class DocsForm(Form):
     boleto       =  FileField('boleto')
     comprovante  =  FileField('comprovante')
     outros       =  FileField('outros')


class RelForm(Form):
     efetuado    =  BooleanField('efetuado')
#posted_date = DateField('Posted Date (mm/dd/yyyy)',validators=[required()],format='%m/%d/%Y')


class PesqForm(Form):
      campo      = StringField('campo', validators = [DataRequired()])
       