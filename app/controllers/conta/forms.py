from flask_wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField
from wtforms.validators import DataRequired

class ContaForm(Form):
     
     bancos = [
                 '01 – Banco do Brasil S.A.',
                 '341 – Banco Itaú S.A.',
                 '033 – Banco Santander (Brasil) S.A.',
                 '356 – Banco Real S.A. (antigo)',
                 '652 – Itaú Unibanco Holding S.A.',
                 '237 – Banco Bradesco S.A.',
                 '745 – Banco Citibank S.A.',
                 '399 – HSBC Bank Brasil S.A. – Banco Múltiplo',
                 '104 – Caixa Econômica Federal',
                 '389 – Banco Mercantil do Brasil S.A.',
                 '453 – Banco Rural S.A.',
                 '422 – Banco Safra S.A.',
                 '633 – Banco Rendimento S.A.'
              ]

     tipos = [

                 'Conta Corrente',
                 'Conta Poupança',
                 'Cartão de Crédito'
             ]

     
     lista_banco = [(k,k) for k in bancos]
     lista_tipo  = [(k,k) for k in tipos ]     

     banco     = SelectField('banco', choices=lista_banco)
     tipo      = SelectField('tipo', choices=lista_tipo)
     agencia   = StringField('agencia')
     conta     = StringField('conta')
     numero    = StringField('numero')
     bandeira  = StringField('bandeira')

