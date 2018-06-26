import os
from app import db
from flask_login import login_required, current_user
from flask_babel import format_currency, format_decimal
from app.controllers.planejamento.forms import PlanejamentoForm
from app.model import Planejamento, Categoria, Usuario, Empresa, Movimentacao, Alert
from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for

planejamento = Blueprint('planejamento',__name__)

@planejamento.route('/index')
@planejamento.route('/')
@login_required
def index():
    session['tela'] = 'planejamento'
    todos = Planejamento.query.filter(Planejamento.empresa_id == session['empresa']).all()
    set_alerts(session['empresa'])
    return render_template('planejamento/index.html', title = 'Meus Planejamentos', todos = todos)

@planejamento.route('/new', methods = ['GET','POST'])
@login_required
def new():
    form = PlanejamentoForm()
    form.categoria_id.choices = [(h.id, str(h.id) + ' ' + h.titulo) for h in Categoria.query.filter(Categoria.empresa_id == session['empresa']).all()]
    
    if form.validate_on_submit():
        plan = Planejamento(
            titulo = form.titulo.data,
            valor  = form.valor.data,
            descricao = form.descricao.data,
            categoria_id = form.categoria_id.data
        )
        plan.empresa_id = session['empresa']
        plan.add(plan)
        set_alerts(session['empresa'])
        return redirect(url_for('planejamento.index'))
    return render_template('planejamento/new.html', title = 'Meus Planejamentos', form = form)

@planejamento.route('/edit/<int:plan_id>', methods = ['GET','POST'])
@login_required
def edit(plan_id):
    plan = Planejamento.query.get(plan_id)
    form = PlanejamentoForm(obj=plan)
    form.categoria_id.choices = [(h.id,h.titulo) for h in Categoria.query.all()]
    if form.validate_on_submit():
        plan.titulo     = form.titulo.data
        plan.valor 	   = form.valor.data
        plan.descricao  = form.descricao.data
        plan.categoria_id = form.categoria_id.data
        plan.update()
        set_alerts(session['empresa'])
        return redirect(url_for('planejamento.index'))
    return render_template('planejamento/edit.html', title = 'Alterar Planejamento', form = form)

@planejamento.route('/delete/<int:plan_id>')
@login_required
def delete(plan_id):
    plan = Planejamento.query.get(plan_id)
 
    # Verificar se existe movimentação do usuário antes de apagar ou apagar todas as movimentacoes
    plan.delete(plan)
    set_alerts(session['empresa'])
    return redirect(url_for('planejamento.index'))

@planejamento.context_processor
def dados():
    empresa = Empresa.query.get(session['empresa'])
    usuario = Usuario.query.get(current_user.id)
    set_alerts(session['empresa'])
    return dict(empresa = empresa.nome, usuario = usuario.nome)

def formatar_dinheiro(value):
    if type(value) == str:
        value = int(value)
    
    valor = format_decimal(value, format='#.##,##;(#)')
    return 'R$ {}'.format(valor)

def set_alerts(empresa_id):
    session['alerts'] = []
    plans = Planejamento.query.filter(Planejamento.empresa_id == empresa_id).all()
    if len(plans) > 0:
        for plan in plans:
            movs = Movimentacao.query.filter(Movimentacao.categoria_id == plan.categoria_id).all()
            
            sum_valor_movs = 0
            for mov in movs:
                sum_valor_movs = sum_valor_movs + abs(mov.valor)
            
            if sum_valor_movs >= plan.valor:
                session['alerts'].append(plan.titulo + ' - Valor Limite: ' + formatar_dinheiro((plan.valor)) + ' - Valor Atual: ' + formatar_dinheiro((sum_valor_movs)))