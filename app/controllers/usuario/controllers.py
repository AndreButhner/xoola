from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from werkzeug import secure_filename
from app import db
from app.controllers.usuario.forms import UserForm
from app.model import Usuario,Empresa
from flask_login import login_required




usuario = Blueprint('usuario',__name__)

@usuario.route('/index')
@usuario.route('/')
@login_required
def index():
    session['tela'] = "usuario"
    todos = Usuario.query.all() 
    return render_template('usuario/index.html',title='Lista de Usuario',todos=todos)


@usuario.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = UserForm()    
    form.empresa_id.choices = [(h.id,h.nome) for h in Empresa.query.all()]
    if form.validate_on_submit():
       user = Usuario(
                           nome       = form.nome.data,
                           sobrenome  = form.sobrenome.data,
                           email      = form.email.data,
                           login      = form.login.data,
                           password   = form.password.data,
                           empresa_id = form.empresa_id.data
                          )
       print(user.add(user))
       return redirect(url_for('usuario.index'))
    return render_template('usuario/new.html',title='Cadastro de Usuario',form=form)



@usuario.route("/edit/<int:user_id>", methods = ["GET","POST"])
@login_required
def edit(user_id):
    user = Usuario.query.get(user_id)
    src_path = user.empresa.nome + '/' + user.nome
    form = UserForm(obj=user)
    form.empresa_id.choices = [(h.id,h.nome) for h in Empresa.query.all()]
    if form.validate_on_submit():
       user.nome       = form.nome.data
       user.sobrenome  = form.sobrenome.data
       user.email      = form.email.data
       user.login      = form.login.data
       user.password   = form.password.data
       user.empresa_id = form.empresa_id.data

       
       user.update()
       return redirect(url_for('usuario.index'))
    return render_template("usuario/edit.html",title='Alterar de Empresa', form=form)

@usuario.route("/delete/<int:user_id>")
@login_required
def delete(user_id):
    user = Usuario.query.get(user_id)
 
    # Verificar se existe movimentação do usuário antes de apagar ou apagar todas as movimentacoes
    user.delete(user)
    return redirect(url_for('usuario.index'))


