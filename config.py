import os

WTF_CSRF_ENABLED=True
SECRET_KEY = "you-will-never-guess"


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/banco_de_dados.db')
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:nisled@localhost/xoola'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True

# upload_documentos

UPLOAD_FOLDER = os.path.join(basedir,"app/static/docs_repository/xoola")



#Timezone
BABEL_DEFAULT_LOCALE='br'
BABEL_DEFAULT_TIMEZONE='UTC'

#EMAIL SETTINGS
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587
MAIL_USE_SSL=False
MAIL_USE_TLS=True
MAIL_USERNAME = 'clodonil@decoroecsa.com.br'
MAIL_PASSWORD = 'AkugF176.'


#celery
#CELERY_IMPORTS = ('app.tasks')
CELERY_IGNORE_RESULT = False
BROKER_HOST = "127.0.0.1" #IP address of the server running RabbitMQ and Celery
BROKER_PORT = 5672
BROKER_URL='amqp://'
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS=("app.crontab",)


from celery.schedules import crontab
 
CELERYBEAT_SCHEDULE = {
    'minuto': {
        'task': 'app.crontab.contas_fixas',                             
        'schedule': crontab(minute='*/1'),     
    },
    'every-minute': {
        'task': 'app.crontab.finalizar_contas',
        'schedule': crontab(minute='5'),
        
    },

    'day': {
        'task': 'app.crontab.ordem_pagamento',
        'schedule': crontab(hour='3', minute='00'),
        
    },


}
