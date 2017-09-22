#!/bin/bash


rm -rf db_repository
rm -rf db/banco_de_dados.db
rm -rf /opt/flask/Projetos/xoolo/app/static/docs_repository/*


./db_create.py
./db_migrate.py

./populando.py
