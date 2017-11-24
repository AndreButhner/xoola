#coding: utf-8

import os
from flask import Flask, Blueprint, redirect,url_for, render_template
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from config import basedir
from celery import Celery




app = Flask(__name__)
app.config.from_object('config')

#celery

celery = Celery(app.name, broker=app.config['BROKER_URL'])
#celery.config_from_object('celeryconfig')
celery.conf.update(app.config)


babel = Babel(app)

# Banco de Dados
db = SQLAlchemy(app)


# Servidor de Email
mail = Mail(app)



# Basic Routes #

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Autenticação
login_manager = LoginManager()
login_manager.init_app(app)

# Modulos
from app import model
from app.controllers.auth.controllers import auth
from app.controllers.empresa.controllers import empresa
from app.controllers.conta.controllers import conta
from app.controllers.planejamento.controllers import planejamento
from app.controllers.usuario.controllers import usuario
from app.controllers.categoria.controllers import categoria
from app.controllers.movimentacao.controllers import movimentacao
from app.controllers.relatorio.controllers import relatorio
from app.controllers.upload.controllers import upload
from app.controllers.dashboard.controllers import dashboard


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(empresa, url_prefix='/empresa')
app.register_blueprint(conta, url_prefix='/conta')
app.register_blueprint(planejamento, url_prefix='/planejamento')
app.register_blueprint(usuario, url_prefix='/usuario')
app.register_blueprint(categoria, url_prefix='/categoria')
app.register_blueprint(movimentacao, url_prefix='/movimentacao')
app.register_blueprint(relatorio, url_prefix='/relatorio')
app.register_blueprint(upload, url_prefix='/upload')
app.register_blueprint(dashboard, url_prefix='/dashboard')




@app.context_processor
def utility_processor():
    def formatar_dinheiro(value):
        if type(value) == str:
           value = int(value)
        #return "R$ {}".format(str(format_currency(value,'BR',format='#.##0,##')))
        valor = format_decimal(value, format='#.##,##;(#)')
        return "R$ {}".format(valor)
    return dict(formatar_dinheiro=formatar_dinheiro)



