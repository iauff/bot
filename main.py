#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Arquivo para publicar um serviço web baseado no framework flask.

import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/webhook')
def WelcomeToMyapp():
    return 'Bem-vindo a minha app!'

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
