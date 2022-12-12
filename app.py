#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 06:26:15 2022

@author: sdas
"""

import flask
from blueprint_module import blueprint
 
app = flask.Flask(__name__,static_url_path='/',static_folder='./client/build')
app.register_blueprint(blueprint)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

#homepage
@app.route('/',methods=['GET'])
def index():
    return app.send_static_file('index.html')

if __name__=='__main__':
    app.run()