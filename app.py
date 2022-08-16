#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 06:26:15 2022

@author: sdas
"""

import flask
from flask import request
from datetime import datetime as dt
from dateutil import parser

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    x = str(request.args['text'])
    y=parser.parse(x, fuzzy=True)
    try:
        return y
    except KeyError:
        return 'bye'