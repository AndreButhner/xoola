from app import db
from app.controllers.categoria.forms import CatForm
from flask_login import login_required, current_user
from flask_babel import format_currency, format_decimal
from app.model import Categoria, Empresa, Usuario, Planejamento, Movimentacao, Alert
from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for

categoria = Blueprint('categoria',__name__)

@categoria.route('/index')
@categoria.route('/')
@login_required
def index():
    session['tela'] = 'categoria'
    todos = Categoria.query.filter(Categoria.empresa_id == session['empresa'] ).all()
    set_alerts(session['empresa'])
    return render_template('categoria/index.html', title = 'Lista de Categorias', todos = todos)

@categoria.route('/new', methods = ['GET','POST'])
@login_required
def new():
    form = CatForm()
    if form.validate_on_submit():
        cat = Categoria(
            titulo     = form.titulo.data,
            descricao  = form.descricao.data,
            keywords   = form.titulo.data,
            status     = form.status.data
        )
        cat.empresa_id = session['empresa']
        cat.add(cat)
        return redirect(url_for('categoria.index'))
    return render_template('categoria/new.html', title = 'Cadastro de Novas Contas', form = form)

@categoria.route('/edit/<int:cat_id>', methods = ['GET','POST'])
@login_required
def edit(cat_id):
    cat = Categoria.query.get(cat_id)
    form = CatForm(obj = cat)
    if form.validate_on_submit():
        cat.titulo     = form.titulo.data
        cat.descricao  = form.descricao.data
        cat.status     = form.status.data
        cat.update()
        return redirect(url_for('categoria.index'))
    return render_template('categoria/edit.html', title = 'Alterar de Empresa', form = form)

@categoria.route('/delete/<int:cat_id>')
@login_required
def delete(cat_id):
    cat = Categoria.query.get(cat_id)
    # Verifica se existe movimentação do usuário antes de apagar uma categoria
    movs = Movimentacao.query.filter(Movimentacao.categoria_id == cat_id).all()
    if len(movs) == 0:
        cat.delete(cat)
    return redirect(url_for('categoria.index'))

@categoria.context_processor
def dados():
    usuario = Usuario.query.get(current_user.id)
    empresa = Empresa.query.get(session['empresa'])
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



