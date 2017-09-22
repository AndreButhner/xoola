import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_EXTRATO = 'app/static/docs_repository/extrato'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_EXTRATO'] = UPLOAD_EXTRATO