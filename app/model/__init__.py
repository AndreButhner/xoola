from app import db
from datetime import datetime
#from flask_login import LoginManager, login_user,UserMixin, logout_user
from sqlalchemy.sql.expression import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import INET
from werkzeug import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from config import UPLOAD_FOLDER
import os


# Relacionamento de many to many entre a tabela movimento e docs
Mov_Docs = db.Table('Mov_Docs',
    db.Column('movimentacao_id', db.Integer, db.ForeignKey('movimentacao.parcelas_id'), nullable=False),
    db.Column('docs_id', db.Integer, db.ForeignKey('docs.id'), nullable=False),
    db.PrimaryKeyConstraint('movimentacao_id', 'docs_id')
)  


class Movimentacao(db.Model):
      id                = db.Column(db.Integer, primary_key=True)
      titulo            = db.Column(db.String(100), index=True)
      descricao         = db.Column(db.String(255), index=True)      
      valor             = db.Column(db.Float)
      juros             = db.Column(db.Float,default=0)
      multa             = db.Column(db.Float,default=0)
      desconto          = db.Column(db.Float,default=0)
      data_v            = db.Column(db.Date)
      data_pagamento    = db.Column(db.Date)
      parcelas          = db.Column(db.Integer)
      parcelas_id       = db.Column(db.Integer)
      efetuado          = db.Column(db.Boolean)
      finalizada        = db.Column(db.Boolean, default=False)
      categoria_id      = db.Column(db.Integer, db.ForeignKey('categoria.id'))
      formapagamento_id = db.Column(db.Integer, db.ForeignKey('formapagamento.id'))
      empresa_id        = db.Column(db.Integer, db.ForeignKey('empresa.id'))
      conta_id          = db.Column(db.Integer, db.ForeignKey('conta.id'))
      docs              = db.relationship('Docs', secondary=Mov_Docs,  backref=db.backref('movimentacao',lazy='dynamic'))     
      date_created      = db.Column(db.DateTime)
      date_modified     = db.Column(db.DateTime)

     
      def __repr__(self):
          return '<Movimentacao %r>' %(self.titulo)

      def __init__(self,titulo, descricao, valor, data_v, parcelas, categoria_id,formapagamento_id,conta_id):
          self.titulo         = titulo
          self.descricao      = descricao
          self.valor          = valor
          self.data_v         = data_v
          self.parcelas       = parcelas
          self.categoria_id   = categoria_id
          self.formapagamento_id = formapagamento_id
          self.conta_id       = conta_id
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()

      def get_id(self):
          return str(self.id)

      def add(self,movimentacao):
          db.session.add(movimentacao)
          return session_commit()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,movimentacao):
          db.session.delete(movimentacao)
          return session_commit()
  





class Docs(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      filename      = db.Column(db.String(100), index=True)
      path          = db.Column(db.String(255), index=True)
      tipo          = db.Column(db.String(100))
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)

      def __repr__(self):
          return '<Docs %r>' %(self.filename)

      def __init__(self,filename, path, tipo):
          self.filename       = filename
          self.path           = path
          self.tipo           = tipo
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()


      def get_id(self):
          return str(self.id)

      def add(self,docs):
          db.session.add(docs)
          return session_commit ()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,docs):
          db.session.delete(docs)
          return session_commit()


class Formapagamento(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      tipo          = db.Column(db.String(100))
      Movimentacao  = db.relationship('Movimentacao', backref='formapagamento', lazy='dynamic')
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)

      def __repr__(self):
          return '<FormaPagamento %r>' %(self.tipo)

      def __init__(self, tipo):
          self.tipo           = tipo
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()



      def get_id(self):
          return str(self.id)

      def add(self,forma):
          db.session.add(forma)
          return session_commit ()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,forma):
          db.session.delete(forma)
          return session_commit()



class Categoria(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      titulo        = db.Column(db.String(100), index=True)
      descricao     = db.Column(db.String(255), index=True)
      status        = db.Column(db.Integer)
      empresa_id    = db.Column(db.Integer, db.ForeignKey('empresa.id'))     
      Movimentacao  = db.relationship('Movimentacao', backref='categoria', lazy='dynamic')
      Planejamento  = db.relationship('Planejamento', backref='categoria', lazy='dynamic')
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)


      def __repr__(self):
          return '<Categoria %r>' %(self.titulo)


      def __init__(self,titulo, descricao, status):
          self.titulo         = titulo
          self.descricao      = descricao
          self.status         = status
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()

          

      def get_id(self):
          return str(self.id)

      def add(self,cat):
          db.session.add(cat)
          return session_commit ()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,cat):
          db.session.delete(cat)
          return session_commit()


class Usuario(db.Model,UserMixin):
      id            = db.Column(db.Integer, primary_key=True)
      nome          = db.Column(db.String(100), index=True)
      sobrenome     = db.Column(db.String(255), index=True)
      email         = db.Column(db.String(100), unique=True, index=True)      
      password      = db.Column(db.String(100), index=True)
      login         = db.Column(db.String(100))      
      empresa_id    = db.Column(db.Integer, db.ForeignKey('empresa.id'))      
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)


      def __repr__(self):
          return '<Usuario %r>' %(self.nome)


      def __init__(self,nome, sobrenome, email,login, password, empresa_id):
          self.nome           = nome
          self.sobrenome      = sobrenome
          self.email          = email.lower()  
          self.login          = login       
          self.set_password(password)
          self.empresa_id     = empresa_id
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()


      
      def add(self,user):
          db.session.add(user)
          session_commit()          
          return True
          

      def update(self):
          self.set_password(self.password)
          self.date_modified  = datetime.utcnow()
          return session_commit()


      def delete(self,user):          
          db.session.delete(user)
          return session_commit()
     
      def set_password(self, password):
          self.password = generate_password_hash(password)
   
      def check_password(self, password):
          return check_password_hash(self.password, password)

class Empresa(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      nome          = db.Column(db.String(100), index=True)
      nome_resp     = db.Column(db.String(100), index=True)
      email         = db.Column(db.String(100), index=True)
      telegram      = db.Column(db.String(100), index=True)
      Usuario       = db.relationship('Usuario', backref='empresa', lazy='dynamic')
      Movimentacao  = db.relationship('Movimentacao', backref='empresa', lazy='dynamic')
      Categoria     = db.relationship('Categoria', backref='empresa', lazy='dynamic')
      #Planejamento  = db.relationship('Planejamento', backref='empresa', lazy='dynamic')
      Conta         = db.relationship('Conta', backref='empresa', lazy='dynamic')
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)


      def __repr__(self):
          return '<Categoria %r>' %(self.nome)


      def __init__(self,nome, email, nome_resp, telegram):
          self.nome           = nome
          self.email          = email
          self.nome_resp      = nome_resp
          self.telegram       = telegram
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()



      def get_id(self):
          return str(self.id)

      def add(self,emp):
          db.session.add(emp)
          create_dir(emp.nome)
          return session_commit()

      def update(self,src,dst):
          self.date_modified  = datetime.utcnow()
          edit_dir(src,dst)
          return session_commit()

      def delete(self,emp):
          db.session.delete(emp)
          delete_dir(emp.nome)
          return session_commit()


class Conta(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      banco         = db.Column(db.String(100))
      tipo          = db.Column(db.String(100))
      agencia       = db.Column(db.String(100))
      conta         = db.Column(db.String(100))
      numero        = db.Column(db.String(100))
      bandeira      = db.Column(db.String(100))
      empresa_id    = db.Column(db.Integer, db.ForeignKey('empresa.id')) 
      movimentacao  = db.relationship('Movimentacao', backref='conta', lazy='dynamic')
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)


      def __repr__(self):
          return '<Conta %r>' %(self.banco)


      def __init__(self,banco, tipo, agencia, conta, numero, bandeira):
          self.banco          = banco
          self.tipo           = tipo
          self.agencia        = agencia
          self.conta          = conta
          self.numero         = numero
          self.bandeira       = bandeira
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()



      def get_id(self):
          return str(self.id)

      def add(self,emp):
          db.session.add(emp)
          return session_commit()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,emp):
          db.session.delete(emp)
          return session_commit()

class Mtelegram(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      usuario       = db.Column(db.String(100))
      id_mensagem   = db.Column(db.String(100))
      tipo_mensagem = db.Column(db.String(100))
      path_file     = db.Column(db.String(100))
      mensagem      = db.Column(db.String(200))
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)


      def __repr__(self):
          return '<Mtelegram %r>' %(self.usuario)


      def __init__(self,usuario, id_mensagem, tipo_mensagem, path_file, mensagem):
          self.usuario        = usuario
          self.id_mensagem    = id_mensagem
          self.tipo_mensagem  = tipo_mensagem
          self.path_file      = path_file
          self.mensagem       = mensagem 
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()



      def get_id(self):
          return str(self.id)

      def add(self,emp):
          db.session.add(emp)
          return session_commit()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,emp):
          db.session.delete(emp)
          return session_commit()


#Universal functions

def  session_commit():
      try:
        db.session.commit()
      except SQLAlchemyError as e:             
         db.session.rollback()
         reason=str(e)
         return reason


def create_dir(path_dir):
    path = UPLOAD_FOLDER+"/"+ path_dir.lower()
    print(path)
    if not os.path.exists(path):
       os.makedirs(path)    

def delete_dir(path_dir):
    src_path = UPLOAD_FOLDER+"/"+ path_dir.lower()
    dst_path = UPLOAD_FOLDER+"/"+ path_dir.lower() + '_deletado'
    if os.path.exists(src_path):
       os.rename(src_path,dst_path)    

def edit_dir(src_path,dst_path):
    src_path = UPLOAD_FOLDER+"/"+ src_path.lower()
    dst_path = UPLOAD_FOLDER+"/"+ dst_path.lower()
    if os.path.exists(src_path):
       os.rename(src_path,dst_path)


class Planejamento(db.Model):
    id                = db.Column(db.Integer, primary_key=True)
    titulo            = db.Column(db.String(100))
    valor             = db.Column(db.Float)
    descricao         = db.Column(db.String(255))
    categoria_id      = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    empresa_id    = db.Column(db.Integer, db.ForeignKey('empresa.id'))
         
    

    def __repr__(self):
        return '<Planejamento %r>' %(self.titulo)


    def __init__(self,titulo, valor, descricao, categoria_id):
        self.titulo = titulo
        self.valor  = valor
        self.descricao = descricao
        self.categoria_id = categoria_id
          
    def get_id(self):
        return str(self.id)

    def add(self,emp):
        db.session.add(emp)
        return session_commit()

    def update(self):
        self.date_modified  = datetime.utcnow()
        return session_commit()

    def delete(self,emp):
        db.session.delete(emp)
        return session_commit()







Upl_Docs = db.Table('Upl_Docs',
    db.Column('upload_id', db.Integer, db.ForeignKey('upload.extrato_id'), nullable=False),
    db.Column('docs_id', db.Integer, db.ForeignKey('docs.id'), nullable=False),
    db.PrimaryKeyConstraint('upload_id', 'docs_id')
)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    extrato_id = db.Column(db.Integer)
    descricao = db.Column(db.String(100))
    efetuado = db.Column(db.Boolean)
    docs = db.relationship('Docs', secondary=Upl_Docs,  backref=db.backref('upload',lazy='dynamic'))
    empresa_id    = db.Column(db.Integer, db.ForeignKey('empresa.id'))
     


    def __repr__(self):
        return '<Conta %r>' %(self.banco)


    def __init__(self,descricao):
        self.descricao = descricao



    def get_id(self):
        return str(self.id)

    def add(self,emp):
        db.session.add(emp)
        return session_commit()

    def update(self):
        self.date_modified  = datetime.utcnow()
        return session_commit()

    def delete(self,emp):
        db.session.delete(emp)
        return session_commit()