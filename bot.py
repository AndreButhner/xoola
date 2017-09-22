#!env/bin/python
# encoding: utf-8

from app import db
from app.model import Categoria, Movimentacao, Docs, Usuario, Empresa, Formapagamento, Mtelegram
import datetime
from dateutil.relativedelta import relativedelta
from config import UPLOAD_FOLDER
from sqlalchemy import func
import telegram
#import img2pdf
import os

#bot.sendMessage(chat_id=chat_id, text="*bold* _italic_ [link](http://google.com).", parse_mode=telegram.ParseMode.MARKDOWN)
#bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)

class Report:
    def __init__(self):
       self.bot = telegram.Bot('140262471:AAGE_zx5Gd8ZHou8ZVXCCzmDddI7KIDSiME')
       

    def open_mensagem(self):
        mensagens = self.bot.getUpdates()
        return mensagens

    def pdf(self, image):
       filename = image
       filepdf = filename.split(".")[0]
       filepdf = filepdf+".pdf"
       pdf_bytes = img2pdf.convert([filename])
       pdf = open(filepdf,'wb')
       pdf.write(pdf_bytes)
       os.remove(filename)


    def send_mensagem(self, mensagem):  
        chat_id = self.bot.getUpdates()[-1].message.chat_id
        self.bot.sendMessage(chat_id=chat_id, text=mensagem)


    def gerar_relatorio(self, empresa):
        pass

    def upload_dados(self,dados):
        for item in dados:
              id_mensagem   = item.message.message_id
              if not Mtelegram.query.filter_by(id_mensagem=id_mensagem).first():
                   suario       = item.message.chat.username
                   empresa       = Empresa.query.filter_by(telegram=usuario).first()
                   mensagem      = ""
                   tipo_mensagem = "file"
                   path_file     = ""

                   if item.message.photo:
                      file_id  = item.message.photo[3].file_id
                      filename = UPLOAD_FOLDER +  "/" + empresa.nome.lower() +"/"+empresa.nome.lower()+"_" + str(id_mensagem) + ".jpg"
                  
                   if item.message.document:
                      file_id   = item.message.document.file_id                 
                      filename  = UPLOAD_FOLDER + "/" + empresa.nome.lower() + "/bot/" + item.message.document.file_name

                   if item.message.photo or item.message.document:   
                      # Salvar o arquivo
                      newFile   = self.bot.getFile(file_id)
                      newFile.download(filename)
                      #self.pdf(filename)

                   if item.message.text:
                      messagem      = item.message.text
                      tipo_mensagem = "texto"
                 
              
                   mensg = Mtelegram(usuario, id_mensagem, tipo_mensagem, path_file, mensagem)     
                   mensg.add(mensg)              
                 
     
    def router(self, msg):
        pass

    def carga(self,msg):

      print(msg)
      titulo            = ""
      descricao         = ""
      valor             = ""
      data              = datetime.date.today()
      parcelas          = ""
      categoria_id      = ""
      formapagamento_id = ""
      

            
      #mov = Movimentacao(
      #                    titulo,
      #                    descricao,
      #                    valor,
      #                    hoje,
      #                    parcelas,
      #                    categoria_id,
      #                    formapagamento_id
      #                   )
#
#      mov.add(mov)
#      mov.parcelas_id = mov.id
#      mov.empresa_id  = empresa_id



    def run(self):
        self.upload_dados(self.open_mensagem())


    def mens(self):
        for mens in Mtelegram.query.all():
            self.router(mens)

            

if __name__ == "__main__":
   new = Report()
   new.run()
