from app import db
from sqlalchemy import extract
from datetime import datetime, timedelta, date
from app.controllers.relatorio.forms import PesForm
from flask_login import login_required, current_user
from flask_babel import format_currency, format_decimal
from app.model import  Conta, Empresa, Usuario, Movimentacao, Categoria, Planejamento, Alert
from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for

relatorio = Blueprint('relatorio',__name__)

@relatorio.route('/index', methods = ['GET','POST'])
@relatorio.route('/', methods=['GET','POST'])
@login_required
def index():
    session['tela'] = 'relatorio'
    
    filter_query = []
    hoje = date.today()
    
    form = PesForm()

    categoria = []
    categoria.append(('0', 'Todos'))
    
    cats = Categoria.query.filter(Categoria.empresa_id == session['empresa']).all()
    if len(cats) > 0:
        for cat in cats:
            categoria.append((cat.id, str(cat.id) + ' ' + cat.titulo))

    form.categoria_id.choices = categoria

    conta =  []
    conta.append(('0', 'Todos'))
    cts = Conta.query.filter(Conta.empresa_id == session['empresa']).all()
    for ct in cts:
        conta.append((ct.id, h.tipo + ' - ' + ct.conta))

    form.conta_id.choices = conta

    if request.method == 'POST':
        if form.categoria_id.data != '0':
            filter_query.append(Movimentacao.categoria_id == form.categoria_id.data)

        if form.conta_id.data != '0':
            filter_query.append(Movimentacao.conta_id == form.conta_id.data)

        if form.data.data:
            (data_inicio,data_fim) = form.data.data.replace(' ','').split('-')

            data_inicio  = datetime.strptime(data_inicio, '%m/%d/%Y') + timedelta(days = -1)
            data_fim     = datetime.strptime(data_fim, '%m/%d/%Y')

            filter_query.append(Movimentacao.data_v >= data_inicio)
            filter_query.append(Movimentacao.data_v <= data_fim)
        else:
            filter_query.append(extract('month', Movimentacao.data_v) == hoje.month)
            filter_query.append(extract('year' , Movimentacao.data_v) == hoje.year)

        # realizando a query no banco de dados
        todos = Movimentacao.query.filter(
            Movimentacao.empresa_id == session['empresa'],
            *filter_query,
        ).order_by('data_v').all()
    else:
        todos = Movimentacao.query.filter(
            Movimentacao.empresa_id == session['empresa'],
            extract('month', Movimentacao.data_v) == hoje.month,
            extract('year', Movimentacao.data_v) == hoje.year
        ).order_by('data_v').all()
    credito = sum([item.valor  for item in todos if item.categoria.status == 0])
    debito = sum([item.valor  for item in todos if item.categoria.status == 1])
    return render_template('relatorio/index.html', title = 'Relatório de Contas', form = form, todos = todos, credito = credito, debito = debito)

@relatorio.route('/dashboard')
@login_required
def dash():
    return render_template('relatorio/dash.html', title = 'Relatório de Contas')

@relatorio.context_processor
def dados():
    usuario = Usuario.query.get(current_user.id)
    empresa = Empresa.query.get(session['empresa'])
    set_alerts(session['empresa'])
    return dict(empresa = empresa.nome, usuario = usuario.nome)

def formatar_dinheiro(value):
    if type(value) == str:
        value = int(value)

    valor = format_decimal(value, format='#.##.##;(#)')
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

