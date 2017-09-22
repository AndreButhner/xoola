from flask_wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField
from wtforms.validators import DataRequired

class CatForm(Form):

     titulo    = StringField('titulo', validators=[DataRequired()])
     descricao = StringField('titulo', validators=[DataRequired()])
     status    = SelectField('Tipo de Conta', choices=[('0','Entrada'),('1','Saída')])



