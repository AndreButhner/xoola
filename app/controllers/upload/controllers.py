from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from sqlalchemy.sql import func
from werkzeug import secure_filename
from app import db
#from app.controllers.movimentacao.forms import MovForm, MovRealizadoForm, DocsForm, RelForm, PesqForm
from app.controllers.upload.forms import UploadExtratoForm, UploadDocForm, UploadRealizadoForm, ExtratoInfo
from app.model import Docs, Upload, Movimentacao
#from config import UPLOAD_FOLDER
from configExtrato import UPLOAD_EXTRATO, ALLOWED_EXTENSIONS, app
from flask_login import login_required, current_user
from flask_babel import format_currency, format_decimal
import datetime
from app.crontab import cad_parcelado
from flask import send_from_directory, Flask, request, jsonify
import os
import pyexcel as pe
import csv
from openpyxl import load_workbook


upload = Blueprint('upload',__name__)

@upload.route('/index')
@upload.route('')
@login_required
def index():
    session['tela'] = "upload"
    todos = Upload.query.all()
    
    return render_template('upload/index.html',title='Upload de Extrato', todos=todos)




@upload.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = UploadExtratoForm()
    if form.validate_on_submit():
       upl = Upload(
                           descricao = form.descricao.data
                          )

       upl.add(upl)
       return redirect(url_for('upload.index'))
    return render_template('upload/new.html',title='Novos Uploads',form=form)



@upload.route("/realizado", methods = ["GET","POST"])
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
    return render_template("upload/realizado.html",title='Meus Extratos', form=form, upl=upl)



## DOC
@upload.route('/docs', methods=('GET', 'POST'))
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


    return render_template('upload/docs.html',title='Anexo de Movimentação',form=form,upl=upl)


@login_required
def upload_docs(filename,upl,form,tipo):    
    # Tipo
    #  0 - Boleto
    #  1 - Comprovante
    #  2 - Outros
    #  3 - Extrato
    user = current_user.id           
    filename = str(upl.id) + '_' + str(user)+'_'+filename
    #path = UPLOAD_FOLDER+"/"+ mov.empresa.nome.lower()+'/'+Usuario.query.get(user).email.lower() +'/'+filename
    path = UPLOAD_FOLDER+"/"+filename
    if tipo == 3:
       file_tipo = "EXTRATO"
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
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''





@upload.route('/sincronizar', methods=['GET', 'POST'])
def upload_sincronizar():
    wb = load_workbook(filename='/home/andre/Documents/xoola/app/static/docs_repository/extrato/extrato1.xlsx', read_only=True)
    ws = wb['Sheet1']
    lista = (self)

    for row in ws.get_squared_range(min_col=2,max_col=20, min_row=13, max_row=100):
        for cell in row:
            if cell.value != (None):
                lista.append(cell.value)
                #print(cell.value)
    print (lista)







# @upload.route('/realizado/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_EXTRATO'],
#                                filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <h3>Sincronizado</h3>
    </form>
    '''




   




#@upload.route('/sincronizar', methods=['GET', 'POST'])
#def upload_sincronizar():
 #   with open('/home/andre/workspace/xoola/app/static/docs_repository/extrato/extrato1.csv', newline='') as csvfile:
  #     spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
   #    linhas=[] 
    #   for row in spamreader:
     #    linhas.append(row)
         
    #return redirect(url_for('upload.index',filename=filename))
    #return render_template('upload/sincronizar.html',title='Anexo de Movimentação',dados=linhas)