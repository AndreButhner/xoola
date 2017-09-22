from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from werkzeug import secure_filename
from app import db
from app.controllers.planejamento.forms import PlanejamentoForm
from app.model import Planejamento, Categoria
from flask_login import login_required
import os



planejamento = Blueprint('planejamento',__name__)

@planejamento.route('/index')
@planejamento.route('/')
@login_required
def index():	
    session['tela'] = "planejamento"  
    todos = Planejamento.query.filter(Planejamento.empresa_id == session['empresa']).all()
    return render_template('planejamento/index.html',title='Meus Planejamentos',planejamento=todos)
    

@planejamento.route('/new', methods=['GET','POST'])
@login_required
def new():
	form = PlanejamentoForm()
	form.categoria_id.choices = [(h.id,str(h.id) + " " + h.titulo) for h in Categoria.query.filter(Categoria.empresa_id == session['empresa']).all() ]
	if form.validate_on_submit():
	   plan = Planejamento(
								titulo = form.titulo.data,
								valor  = form.valor.data,
								descricao = form.descricao.data,
								categoria_id = form.categoria_id.data								
			                )
	   plan.empresa_id = session['empresa']
	   plan.add(plan)
	   return redirect(url_for('planejamento.index'))
	return render_template('planejamento/new.html',title='Meus Planejamentos',form=form)