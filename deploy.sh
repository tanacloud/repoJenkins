#!/bin/bash

cd /home/ec2-user/flask-app
pip install -r requirements.txt

# Mata qualquer processo Flask rodando antes
pkill -f "flask run"

# Inicia a aplicação Flask
nohup python app.py > flask.log 2>&1 &
