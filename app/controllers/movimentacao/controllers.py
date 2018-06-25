from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from sqlalchemy.sql import func
from werkzeug import secure_filename
from app import db
from app.controllers.movimentacao.forms import MovForm, MovRealizadoForm, DocsForm, RelForm, PesqForm
from app.model import Movimentacao,Docs, Categoria,Formapagamento, Usuario, Empresa, Conta
from config import UPLOAD_FOLDER
from flask_login import login_required, current_user
from flask_babel import format_currency, format_decimal
import datetime
from app.crontab import cad_parcelado
from flask import send_from_directory, Flask, request, jsonify
from configExtrato import ALLOWED_EXTENSIONS, UPLOAD_EXTRATO




movimentacao = Blueprint('movimentacao',__name__)


@movimentacao.route("/index/<int:mov_id>")
@movimentacao.route('/<int:mov_id>')
@login_required
def index(mov_id):
    if mov_id == 0:
       session['tela'] = "entrada"

    elif mov_id == 1:
       session['tela'] = "saida"


    todos = Movimentacao.query.join(Categoria, Movimentacao.categoria_id == Categoria.id).filter(Categoria.status == mov_id,Movimentacao.efetuado == None, Movimentacao.empresa_id == session['empresa'] ).order_by('data_v').all()
    soma  = sum([item.valor  for item in todos])

    #todos = Movimentacao.query.all()
    #todos = Movimentacao.query.order_by(Movimentacao.data_v).all()
    #todos = Movimentacao.query.filter(Movimentacao.efetuado == None, Movimentacao.empresa_id == session['empresa'] ).order_by('data_v').all()
    
    #form = RelForm()
 
    return render_template('movimentacao/index.html',title='Lista de Contas',todos=todos, sum=soma)


@movimentacao.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = MovForm()    
    form.categoria_id.choices = [(h.id,str(h.id) + " " + h.titulo) for h in Categoria.query.filter(Categoria.empresa_id == session['empresa']).all() ]
    form.formapagamento_id.choices = [(h.id,h.tipo) for h in Formapagamento.query.all()]
    form.conta_id.choices = [(h.id,h.tipo + '-' + h.conta) for h in Conta.query.filter(Conta.empresa_id == session['empresa']).all() ]

    if form.validate_on_submit():
       mov = Movimentacao(
                           titulo            = form.titulo.data,
                           descricao         = form.descricao.data,
                           valor             = form.valor.data,
                           parcelas          = form.parcelas.data,
                           data_v            = form.data_v.data,
                           categoria_id      = form.categoria_id.data,                          
                           formapagamento_id = form.formapagamento_id.data,
                           conta_id          = form.conta_id.data
                          )       
       mov.empresa_id = session['empresa']
       mov.add(mov)
       mov.parcelas_id = mov.get_id()
       mov.update()

       #cereley

       cad_parcelado.delay(mov.id)

       if session['tela'] == "entrada":
           mov_id = 0
       else:
           mov_id = 1            
       return redirect(url_for('movimentacao.index',mov_id=mov_id))
    return render_template('movimentacao/new.html',title='Cadastro de Novas Contas',form=form)


## EDIT
@movimentacao.route("/edit/<int:mov_id>", methods = ["GET","POST"])
@login_required
def edit(mov_id):
    mov = Movimentacao.query.get(mov_id)
    form = MovForm(obj=mov)
    form.categoria_id.choices = [(h.id,h.titulo) for h in Categoria.query.all()]
    form.formapagamento_id.choices = [(h.id,h.tipo) for h in Formapagamento.query.all()]
    form.conta_id.choices = [(h.id,h.tipo + '-' + h.conta) for h in Conta.query.all()]

    cat_old_id = mov.categoria_id
    print('cat_old_id: ' + str(cat_old_id))
    cat_new_id = form.categoria_id.data
    print('cat_new_id: ' + str(cat_new_id))
    
    if form.validate_on_submit():
        mov.titulo       = form.titulo.data
        mov.descricao    = form.descricao.data
        mov.valor        = form.valor.data
        mov.parcelas     = form.parcelas.data
        mov.data_v       = form.data_v.data
        mov.categoria_id = form.categoria_id.data                          
        mov.formapagamento_id = form.formapagamento_id.data
        mov.conta_id     = form.conta_id.data
        mov.update()

        if session['tela'] == "entrada":
            mov_id = 0
        else:
            mov_id = 1

        # atualiza as categorias
        cat_old = Categoria.query.get(cat_old_id)
        cat_old.descricao = ''
        movs_cat_old = Movimentacao.query.filter(Movimentacao.categoria_id == cat_old_id).all()
        print('movs_cat_old: ' + str(movs_cat_old))
        if len(movs_cat_old) > 0:
            for m in movs_cat_old:
                if len(movs_cat_old) == 1:
                    cat_old.descricao = m.titulo
                    print('1 - cat_old_desc: ' + cat_old.descricao)
                else:
                    if movs_cat_old.index(m) < (len(movs_cat_old) - 1):
                        cat_old.descricao = cat_old.descricao + m.titulo + ' ; '
                        print('2 - cat_old_desc: ' + cat_old.descricao)
                    else:
                        cat_old.descricao = cat_old.descricao + m.titulo
                        print('3 - cat_old_desc: ' + cat_old.descricao)
            print('final - cat_old_desc: ' + cat_old.descricao)
        cat_old.update()

        cat_new = Categoria.query.get(mov.categoria_id)
        cat_new.descricao = ''
        movs_cat_new = Movimentacao.query.filter(Movimentacao.categoria_id == mov.categoria_id).all()
        print('movs_cat_new: ' + str(movs_cat_new))
        if len(movs_cat_new) > 0:
            for m in movs_cat_new:
                if len(movs_cat_new) == 1:
                    cat_new.descricao = m.titulo
                    print('1 - cat_new_desc: ' + cat_new.descricao)
                else:
                    if movs_cat_new.index(m) < (len(movs_cat_new) - 1):
                        cat_new.descricao = cat_new.descricao + m.titulo + ' ; '
                        print('2 - cat_new_desc: ' + cat_new.descricao)
                    else:
                        cat_new.descricao = cat_new.descricao + m.titulo
                        print('3 - cat_new_desc: ' + cat_new.descricao)
            print('final - cat_new_desc: ' + cat_new.descricao)
        cat_new.update()

        return redirect(url_for('movimentacao.index', mov_id=mov_id))
    return render_template("movimentacao/edit.html",title='Alterar de Lançamento', form=form)


## Realizado
@movimentacao.route("/realizado/<int:mov_id>", methods = ["GET","POST"])
@login_required
def realizado(mov_id):
    mov = Movimentacao.query.get(mov_id)
    form = MovRealizadoForm(valor = mov.valor)
    
    

    if form.validate_on_submit():        
        
         mov.valor          = form.valor.data
         mov.juros          = form.juros.data
         mov.desconto       = form.desconto.data
         mov.multa          = form.multa.data                          
         mov.data_pagamento = form.data_pagamento.data
         mov.efetuado       = True       
         
         filename_c         = secure_filename(form.comprovante.data.filename)         
         if filename_c:
            upload_docs(filename_c,mov,form,1)

         mov.update()


         if session['tela'] == "entrada":
           mov_id = 0
         else:
           mov_id = 1            

         return redirect(url_for('movimentacao.index', mov_id=mov_id))
    return render_template("movimentacao/realizado.html",title='Lançamento', form=form, mov=mov)    


## DELETE
@movimentacao.route("/delete/<int:mov_id>")
@login_required
def delete(mov_id):
    mov = Movimentacao.query.get(mov_id)
 
    # Verificar se existe movimentação do usuário antes de apagar ou apagar todas as movimentacoes
    mov.delete(mov)

    if session['tela'] == "entrada":
       mov_id = 0
    else:
       mov_id = 1            

    return redirect(url_for('movimentacao.index', mov_id=mov_id))


## DOC
@movimentacao.route('/docs/<int:mov_id>', methods=('GET', 'POST'))
@login_required
def docs(mov_id):
    mov = Movimentacao.query.get(mov_id)    
    form = DocsForm()
    if form.validate_on_submit():
       filename_b = secure_filename(form.boleto.data.filename)
       if filename_b:
          upload_docs(filename_b,mov,form,0)           

       filename_c = secure_filename(form.comprovante.data.filename)
       if filename_c:
          upload_docs(filename_c,mov,form,1)    
        
       filename_o = secure_filename(form.outros.data.filename)
       if filename_o:
          upload_docs(filename_o,mov,form,2)    
                 
       db.session.commit()
 
       if session['tela'] == "entrada":
           mov_id = 0
       else:
           mov_id = 1            

       return redirect(url_for('movimentacao.index', mov_id=mov_id))


    return render_template('movimentacao/docs.html',title='Anexo de Movimentação',form=form,mov=mov)

@movimentacao.route('/docs_delete/<int:file_id>', methods=('GET', 'POST'))
@login_required
def docs_delete(file_id):
    file = Docs.query.get(file_id)
    file.delete(file)


    if session['tela'] == "entrada":
       mov_id = 0
    else:
       mov_id = 1            

    return redirect(url_for('movimentacao.index', mov_id=mov_id))


@movimentacao.route("/pesquisa", methods=('GET', 'POST'))
@login_required
def pesquisa():
    session['tela'] = "pesquisa"    
    form = PesqForm()
    if form.validate_on_submit():
       campo = form.campo.data
       todos = Movimentacao.query.filter((Movimentacao.titulo.like("%"+campo+"%")) | (Movimentacao.descricao.like("%"+campo+"%")), Movimentacao.empresa_id == session['empresa'] ).order_by('data_v DESC').all()
    else:
       todos = Movimentacao.query.filter(Movimentacao.efetuado,Movimentacao.empresa_id == session['empresa'] ).order_by('data_v DESC').all()
      
 
    return render_template('movimentacao/pesquisa.html',title='Pesquisa de Contas',todos=todos,form=form)


@login_required
def upload_docs(filename,mov,form,tipo):    
    # Tipo
    #  0 - Boleto
    #  1 - Comprovante
    #  2 - Outros
    user = current_user.id           
    filename = str(mov.id) + '_' + str(user)+'_'+filename
    #path = UPLOAD_FOLDER+"/"+ mov.empresa.nome.lower()+'/'+Usuario.query.get(user).email.lower() +'/'+filename
    path = UPLOAD_FOLDER+"/"+filename
    if tipo == 0:
       file_tipo = "BOLETO"
       form.boleto.data.save(path)
    elif tipo == 1:
       file_tipo = "COMPROVANTE"
       form.comprovante.data.save(path)       
    else:
       file_tipo = "OUTROS"
       form.outros.data.save(path)
    
    
    doc = Docs(filename,path,file_tipo)
    doc.add(doc)
    mov.docs.append(doc)


@login_required
def date_format(view, value):
    return value.strftime('%d/%m/%Y')



@movimentacao.context_processor
def dados():
    empresa = Empresa.query.get(session['empresa'])
    usuario = Usuario.query.get(current_user.id)
    hoje    = datetime.date.today()
    return dict(empresa=empresa.nome, usuario = usuario.nome, hoje=hoje)

@movimentacao.context_processor
def utility_processor():
    def credito():
        hoje = datetime.date.today()         
        '''
            total_dia = Movimentacao.query.with_entities(func.avg(Movimentacao.valor).label('total')).filter(
                  Movimentacao.data_v == hoje, Movimentacao.empresa_id == session['empresa'])
        ''' 
        debito_dia = Movimentacao.query.with_entities(func.sum(Movimentacao.valor)).join(Categoria).filter(
                   Movimentacao.data_v == hoje, Movimentacao.empresa_id == session['empresa'], Categoria.status == 1)

        '''   
        debito_mes = Movimentacao.query.with_entities(func.sum(Movimentacao.valor)).join(Categoria).filter(
                   Movimentacao.data_v.month == hoje.month, Movimentacao.empresa_id == session['empresa'], Categoria.status == 1)
        '''

        debito_mes = 0.0


        credito_dia = Movimentacao.query.with_entities(func.sum(Movimentacao.valor)).join(Categoria).filter(
                   Movimentacao.data_v == hoje, Movimentacao.empresa_id == session['empresa'], Categoria.status == 0)

        if debito_dia[0][0] == None:
           debito_dia = 0.0
        else:
           debito_dia=debito_dia[0][0]    

        if credito_dia[0][0] == None:
           credito_dia = 0.0
        else:
           credito_dia=credito_dia[0][0]

        return(debito_dia, credito_dia, debito_mes)

    def formatar_dinheiro(value):
        if type(value) == str:
           value = int(value)
        #return "R$ {}".format(str(format_currency(value,'BR')))
        valor = format_decimal(value, format='##.###,##')
        return "R$ {}".format(valor)

    def parcelas(parcelas,parcela_id):

        # Staus
        # Parcelas: 5000 para cancelar parcelas
        # Parcelas: 6000 canceladas apos alteracao
        # Parcelas: 7000 Recorrentes já duplicadas
 
        freq  = {
                  1000:'Diário',
                  1200:'Semanal',
                  1300:'A cada 10 dias',
                  1400:'A cada 15 dias',
                  1500:'A cada 28 dias',
                  1600:'Mensal',
                  1700:'Bimestral',
                  1800:'Trimestral',
                  1900:'Quadrimestral',
                  2000:'Semestral',
                  2100:'Anual' 
               } 
        nparcela = Movimentacao.query.filter(Movimentacao.parcelas_id==parcela_id).all()

        if parcelas in freq:
           return "Recorrente {}".format(freq[parcelas])
        elif parcelas == 7000:
           return 'Recorrentes'   
        elif len(nparcela) >= 1:
           return "{} de {}".format(parcelas,len(nparcela))
        

    return dict(formatar_dinheiro=formatar_dinheiro, parcelas=parcelas)



