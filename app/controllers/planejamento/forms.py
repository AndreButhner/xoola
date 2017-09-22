from flask_wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField
from wtforms.validators import DataRequired

class PlanejamentoForm(Form):

	 titulo       = StringField('titulo', validators=[DataRequired()])
	 valor        = FloatField('valor', validators=[DataRequired()])
	 descricao    = TextAreaField('titulo', validators=[DataRequired()])
	 categoria_id = SelectField('categorias',coerce=int)
     