import os
import re
import csv
import pyexcel as pe

from app import db
from sqlalchemy.sql import func
from openpyxl import load_workbook
from werkzeug import secure_filename
from app.crontab import cad_parcelado
from datetime import datetime, timedelta, date
from app.controllers.categoria.forms import CatForm
from flask_login import login_required, current_user
from flask_babel import format_currency, format_decimal
from flask import send_from_directory, Flask, request, jsonify
from configExtrato import UPLOAD_EXTRATO, ALLOWED_EXTENSIONS, app
from app.model import Docs, Upload, Movimentacao, Categoria, Planejamento, Alert, Empresa, Usuario
from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from app.controllers.upload.forms import UploadExtratoForm, UploadDocForm, UploadRealizadoForm, ExtratoInfo

upload = Blueprint('upload',__name__)

@upload.route('/index')
@upload.route('')
@login_required
def index():
    session['tela'] = 'upload'
    todos = Upload.query.all()
    set_alerts(session['empresa'])
    return render_template('upload/index.html', title = 'Upload de Extrato', todos = todos)

@upload.route('/new', methods = ['GET','POST'])
@login_required
def new():
    form = UploadExtratoForm()
    if form.validate_on_submit():
        upl = Upload(
            descricao = form.descricao.data
        )
        upl.add(upl)
        return redirect(url_for('upload.index'))
    return render_template('upload/new.html', title = 'Novos Uploads', form = form)

@upload.route('/realizado', methods = ['GET','POST'])
@login_required
def realizado():
    upl = Upload.query.filter(Upload.empresa_id == session['empresa']).all()
    form = UploadRealizadoForm(descricao = upl.descricao)
    
    if form.validate_on_submit():
        upl.descricao      = form.descricao.data
        mov.efetuado       = True

        filename_c         = secure_filename(form.extrato.data.filename)
        if filename_c:
            upload_docs(filename_c,upl,form,3)
            upl.update()
        return redirect(url_for('upload.index'))
    return render_template('upload/realizado.html', title = 'Meus Extratos', form = form, upl = upl)

@upload.route('/docs', methods = ('GET', 'POST'))
@login_required
def docs():
    upl = Upload.query.filter(Upload.empresa_id == session['empresa']).all()
    print (upl)
    form = UploadDocForm()
    if form.validate_on_submit():
        filename_e = secure_filename(form.extrato.data.filename)
        if filename_e:
            upload_docs(filename_e,upl,form,3)
                
        db.session.commit()
        return redirect(url_for('upload.index'))
    return render_template('upload/docs.html', title = 'Anexo de Movimentação', form = form, upl = upl)

@login_required
def upload_docs(filename, upl, form, tipo):
    # Tipo
    #  0 - Boleto
    #  1 - Comprovante
    #  2 - Outros
    #  3 - Extrato
    user = current_user.id
    filename = str(upl.id) + '_' + str(user)+'_'+filename
    path = UPLOAD_FOLDER+'/'+filename
    if tipo == 3:
        file_tipo = 'EXTRATO'
        form.extrato.data.save(path)            
    
    doc = Docs(filename,path,file_tipo)
    doc.add(doc)
    upl.docs.append(doc)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@upload.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_EXTRATO'], filename))
            return redirect(url_for('upload.index',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
        <p>
            <input type=file name=file>
            <input type=submit value=Upload>
        </p>
    </form>
    '''

def longestSubstringFinder(string1, string2):
    answer = ''
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ''
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ''
    return True if len(answer) > 0 else False


@upload.route('/sincronizar', methods=['GET', 'POST'])
def upload_sincronizar():
    wb = load_workbook(filename='/Users/wellmmer.oliveira/Documents/GitHub/xoola/app/static/docs_repository/extrato/extrato1.xlsx', read_only=True)
    ws = wb['Sheet1']
    lista = []

    for row in ws.get_squared_range(min_col=2,max_col=20, min_row=13, max_row=100):
        lista.append(ExtratoInfo(row))
    
    if len(lista):
        for incoming in lista:
            if incoming.desc != 'SALDO DO DIA':
                print('INCOMING - data: ' + str(incoming.data) + ' - desc :' + incoming.desc + ' - valor: ' + str(incoming.valor) + ' - saldo: ' + str(incoming.saldo))
                
                # pattern = re.compile('[0-9]*[/][0-9]*\b')
                # pattern.match(string)

                mov = Movimentacao(
                    titulo            = incoming.desc,
                    descricao         = '...',
                    valor             = incoming.valor if incoming.valor != (None) else 0,
                    parcelas          = 1,
                    data_v            = incoming.data,
                    formapagamento_id = 1,
                    categoria_id      = -1,
                    conta_id          = 1 if incoming.valor < 0 else 0
                )
                mov.empresa_id = session['empresa']

                categories = Categoria.query.filter(Categoria.empresa_id == session['empresa']).all()

                if len(categories) > 0:
                    print('categorias: ' + str(categories))
                    for cat in categories:
                        if longestSubstringFinder(mov.titulo, cat.keywords) == True:
                            if (mov.valor < 0 and cat.status == 1) or (mov.valor >= 0 and cat.status == 0):
                                print('cat: ' + str(cat))
                                mov.categoria_id = cat.get_id()

                                cat_edited = Categoria.query.get(cat.get_id())
                                cat_edited.keywords = cat_edited.keywords + ' ; ' + incoming.desc
                                cat_edited.update()

                    if mov.categoria_id == -1:
                        if mov.valor < 0:
                            cat_outros_saida = Categoria.query.filter(Categoria.titulo == 'OUTROS - SAIDA' and Categoria.status == 1).first()
                            print('saida: ' + str(cat_outros_saida))
                            if cat_outros_saida != None:
                                mov.categoria_id = cat_outros_saida.get_id()

                                cat_edited = Categoria.query.get(cat_outros_saida.get_id())
                                cat_edited.keywords = cat_edited.keywords + ' ; ' + mov.titulo
                                cat_edited.update()
                            else:
                                new_cat = Categoria(
                                    titulo     = 'OUTROS - SAIDA',
                                    descricao  = 'Lançamentos de saída não definidos',
                                    keywords   = mov.titulo,
                                    status     = 1
                                )
                                new_cat.empresa_id = session['empresa']
                                new_cat.add(new_cat)

                                mov.categoria_id = new_cat.get_id()
                                print('new cat saida: ' + str(new_cat))
                        else:
                            cat_outros_entrada = Categoria.query.filter(Categoria.titulo == 'OUTROS - ENTRADA' and Categoria.status == 0).first()
                            print('entrada: ' + str(cat_outros_entrada))
                            if cat_outros_entrada != None:
                                mov.categoria_id = cat_outros_entrada.get_id()

                                cat_edited = Categoria.query.get(cat_outros_entrada.get_id())
                                cat_edited.keywords = cat_edited.keywords + ' ; ' + mov.titulo
                                cat_edited.update()
                            else:
                                new_cat = Categoria(
                                    titulo     = 'OUTROS - ENTRADA',
                                    descricao  = 'Lançamentos de entrada não definidos',
                                    keywords   = mov.titulo,
                                    status     = 0
                                )
                                new_cat.empresa_id = session['empresa']
                                new_cat.add(new_cat)

                                mov.categoria_id = new_cat.get_id()
                                print('new cat entrada: ' + str(new_cat))
                else:
                    print('categorias vazio: ' + str(categories))
                    if mov.valor < 0:
                        new_cat = Categoria(
                            titulo     = 'OUTROS - SAIDA',
                            descricao  = 'Lançamentos de saída não definidos',
                            keywords   = mov.titulo,
                            status     = 1
                        )
                        new_cat.empresa_id = session['empresa']
                        new_cat.add(new_cat)

                        mov.categoria_id = new_cat.get_id()
                        print('new cat saida: ' + str(new_cat))
                    else:
                        new_cat = Categoria(
                            titulo     = 'OUTROS - ENTRADA',
                            descricao  = 'Lançamentos de entrada não definidos',
                            keywords   = mov.titulo,
                            status     = 0
                        )
                        new_cat.empresa_id = session['empresa']
                        new_cat.add(new_cat)

                        mov.categoria_id = new_cat.get_id()
                        print('new cat entrada: ' + str(new_cat))

                print('movimentacao: ' + str(mov))
                mov.add(mov)
    set_alerts(session['empresa'])    
    return redirect(url_for('movimentacao.index', mov_id = 0))

@upload.context_processor
def dados():
    empresa = Empresa.query.get(session['empresa'])
    usuario = Usuario.query.get(current_user.id)
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