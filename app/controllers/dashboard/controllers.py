from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from app import db
#from app.controllers.dashboard.forms import CatForm
#from app.model import Categoria, Empresa, Usuario
from flask_login import login_required, current_user


dashboard = Blueprint('dashboard',__name__)

@dashboard.route('/index')
@dashboard.route('/')
@login_required
def index():
    session['tela'] = "dash"
    
    return render_template('dashboard/index.html',title='Graficos para controle')