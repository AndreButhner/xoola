from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from app import db
from app.controllers.categoria.forms import CatForm
from app.model import Categoria, Empresa, Usuario
from flask_login import login_required, current_user


categoria = Blueprint('categoria',__name__)

@categoria.route('/index')
@categoria.route('/')
@login_required
def index():
    session['tela'] = "categoria"
    todos = Categoria.query.filter(Categoria.empresa_id == session['empresa'] ).all()
    #todos = Categoria.query.all()
    return render_template('categoria/index.html',title='Lista de Categorias',todos=todos)


@categoria.route('/new', methods=['GET','POST'])
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
    return render_template('categoria/new.html',title='Cadastro de Novas Contas',form=form)

@categoria.route("/edit/<int:cat_id>", methods = ["GET","POST"])
@login_required
def edit(cat_id):
    cat = Categoria.query.get(cat_id)
    form = CatForm(obj=cat)
    if form.validate_on_submit():
       cat.titulo     = form.titulo.data
       cat.descricao  = form.descricao.data
       cat.status     = form.status.data
       cat.update()
       return redirect(url_for('categoria.index'))
    return render_template("categoria/edit.html",title='Alterar de Empresa', form=form)

@categoria.route("/delete/<int:cat_id>")
@login_required
def delete(cat_id):
    cat = Categoria.query.get(cat_id)
 
    # Verificar se existe movimentação do usuário antes de apagar ou apagar todas as movimentacoes
    cat.delete(cat)
    return redirect(url_for('categoria.index'))


@categoria.context_processor
def dados():
    empresa = Empresa.query.get(session['empresa'])
    usuario = Usuario.query.get(current_user.id)
    return dict(empresa=empresa.nome, usuario = usuario.nome)



