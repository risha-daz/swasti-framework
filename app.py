#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 06:26:15 2022

@author: sdas
"""

import flask
from flask import request
from datetime import datetime
from dateutil import parser

from sunpy.coordinates import sun
import math

def convert(x):
    y=0
    try:
        y=parser.parse(x, fuzzy=True)
    except:
        if("now" in x or "today" in x):
            y=datetime.now()
        else:
            print("date not understood")

    if y:
        return math.floor(sun.carrington_rotation_number(y))
    else:
        return 0


app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    x = str(request.args['text'])
    cr=convert(x)
    try:
        return str(cr)
    except KeyError:
        return 'bye'
