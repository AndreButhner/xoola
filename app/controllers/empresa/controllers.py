from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from werkzeug import secure_filename
from app import db
from app.controllers.empresa.forms import EmpForm
from app.model import Empresa
from flask_login import login_required
import os



empresa = Blueprint('empresa',__name__)

@empresa.route('/index')
@empresa.route('/')
@login_required
def index():
    todos = Empresa.query.all()
    session['tela'] = "empresa"
    return render_template('empresa/index.html',title='Lista de Empresas',todos=todos)


@empresa.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = EmpForm()
    if form.validate_on_submit():
       emp = Empresa(
                           nome   = form.nome.data,
                           email  = form.email.data,
                           nome_resp = form.nome_resp.data,
                           telegram  = form.telegram.data
                          )

       emp.add(emp)
       return redirect(url_for('empresa.index'))
    return render_template('empresa/new.html',title='Cadastro de Empresa',form=form)

@empresa.route("/edit/<int:emp_id>", methods = ["GET","POST"])
@login_required
def edit(emp_id):
    emp = Empresa.query.get(emp_id)
    src_path = emp.nome
    form = EmpForm(obj=emp)
    if form.validate_on_submit():
       emp.nome       = form.nome.data
       emp.email      = form.email.data
       emp.nome_resp  = form.nome_resp.data
       emp.telegram   = form.telegram.data
       emp.update(src_path,emp.nome)
       return redirect(url_for('empresa.index'))
    return render_template("empresa/edit.html",title='Alterar de Empresa', form=form)

@empresa.route("/delete/<int:emp_id>")
@login_required
def delete(emp_id):
    emp = Empresa.query.get(emp_id)
    if len(emp.Usuario.all()) == 0:
       emp.delete(emp)
    return redirect(url_for('empresa.index'))



