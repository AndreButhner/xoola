from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from werkzeug import secure_filename
from app import db,login_manager
from app.controllers.auth.forms import LoginForm
from flask_login import login_user,logout_user,LoginManager, UserMixin, current_user, login_required
from app.model import Usuario
import os



auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
@auth.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       login    = form.login.data
       password = form.password.data

       user = Usuario.query.filter_by(login=login).first()

       if user and user.check_password(password):
          login_user(user)
          session['empresa'] = user.empresa.id
          flash('Logged in successfully')
          return redirect(url_for('movimentacao.index',mov_id=1))
       else:
         flash('usuario ou senha invalido')

    return render_template('auth/login.html',title='Autenticação de Usuário', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def user_loader(user_id):
    return Usuario.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))

