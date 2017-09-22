from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from app import db
from app.controllers.conta.forms import ContaForm
from app.model import  Conta, Empresa, Usuario
from flask_login import login_required, current_user


conta = Blueprint('conta',__name__)

@conta.route('/index')
@conta.route('/')

@login_required
def index():
    session['tela'] = "conta"
    todos =Conta.query.filter(Conta.empresa_id == session['empresa'] ).all()
    #todos = Categoria.query.all()
    return render_template('conta/index.html',title='Lista de Contas',todos=todos)


@conta.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = ContaForm()
    if form.validate_on_submit():
       dconta = Conta(
                           banco     = form.banco.data,
                           tipo      = form.tipo.data,
                           agencia   = form.agencia.data,
                           conta     = form.conta.data,
                           numero    = form.numero.data,
                           bandeira  = form.bandeira.data
                          )

       dconta.empresa_id = session['empresa']
       dconta.add(dconta)
       return redirect(url_for('conta.index'))
    return render_template('conta/new.html',title='Cadastro de Novas Contas',form=form)

@conta.route("/edit/<int:conta_id>", methods = ["GET","POST"])
@login_required
def edit(conta_id):
    conta = Conta.query.get(conta_id)
    form  = ContaForm(obj=conta)
    if form.validate_on_submit():
       conta.banco    = form.banco.data
       conta.tipo     = form.tipo.data
       conta.agencia  = form.agencia.data
       conta.conta    = form.conta.data
       conta.numero   = form.numero.data
       conta.bandeira = form.bandeira.data
       conta.update()
       return redirect(url_for('conta.index'))
    return render_template("conta/edit.html",title='Alterar de Conta', form=form)

@conta.route("/delete/<int:conta_id>")
@login_required
def delete(conta_id):
    conta = Conta.query.get(conta_id)
 
    # Verificar se existe movimentação do usuário antes de apagar ou apagar todas as movimentacoes
    conta.delete(conta)
    return redirect(url_for('conta.index'))


@conta.context_processor
def dados():
    empresa = Empresa.query.get(session['empresa'])
    usuario = Usuario.query.get(current_user.id)
    return dict(empresa=empresa.nome, usuario = usuario.nome)



