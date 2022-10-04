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
from gtts import gTTS

import sunpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import html5lib
import sunpy.map
import pfsspy

import requests
from bs4 import BeautifulSoup

import os

def get_date(x):
    return parser.parse(x, fuzzy=True)

def convert(x):
    y=0
    try:
        y=get_date(x)
    except:
        if("now" in x or "today" in x):
            y=datetime.now()
        else:
            print("date not understood")

    if y:
        return math.floor(sun.carrington_rotation_number(y))
    else:
        return 0




#%% Enter the CR and magnetogram

def get_input(cr):
    
    URL = "https://gong.nso.edu/data/magmap/crmap.html"
    r = requests.get(URL)
    
    #cr = 2053           # Carrignton rotation number
    mag = 'GONG'        # Magnetogram type (GONG/HMI)

    soup = BeautifulSoup(r.content, 'html5lib')
    fileurl=''
    alla=soup.find_all("a", href=True)
    data = '' 
    for data in alla:
    	if(str(cr) in data['href']) :
    		fileurl="https://gong.nso.edu"+data['href']

    #%% Magnetogram input for a CR with res = 360 x 180

    gong_map = sunpy.map.Map(fileurl)
    #header = sunpy.io.fits.get_header(fileurl)

    # transforming fits file into sunpy map
    input_map = sunpy.map.Map(gong_map.data- np.mean(gong_map.data), gong_map.meta)

    #%% Define pfsspy Grid

    nrho = 100
    rss = 2.50                      #Setting source surface (ss) = 2.50 Rsun

    #%% Solving PFSS model to get the Output at source surface

    input = pfsspy.Input(input_map, nrho, rss)
    output = pfsspy.pfss(input)

    #%% Plotting

    # Input map at 1.0 R
    m = input.map
    fig = plt.figure()
    ax = plt.subplot(projection=m)
    m.plot(vmax=-50, vmin =50)
    plt.colorbar()
    ax.set_title('Input field')
    plt.savefig("./static/images/inp_"+str(cr)+".png")
    plt.close()
    # Output map at 2.5 R
    ss_br = output.source_surface_br
    fig = plt.figure()
    ax = plt.subplot(projection=ss_br)

    ss_br.plot()
    # Plot the polarity inversion line (i.e. where B changes its sign or where B=0)
    ax.plot_coord(output.source_surface_pils[0])

    plt.colorbar()
    ax.set_title('Source surface magnetic field')
    plt.savefig("./static/images/outp_"+str(cr)+".png")
    plt.close()
    
    if (m):
        return "success"
    else:
        return "fail"

def get_vel(date):
    URL = "https://omniweb.gsfc.nasa.gov/cgi/nx1.cgi?activity=ftp&res=hour&spacecraft=omni2&start_date="+date+"&end_date="+date+"&maxdays=31&vars=8&vars=9&vars=12&vars=14&vars=22&vars=23&vars=24&scale=Linear&view=0&nsum=1&paper=0&charsize=&xstyle=0&ystyle=0&symbol=0&symsize=&linestyle=solid&table=0&imagex=640&imagey=480&color=&back="
    r2 = requests.get(URL)

    soup = BeautifulSoup(r2.content, 'html5lib')

    alla=soup.find_all("a", href=True)
    fileurl = '' 
    data=''
    for data in alla:
    	if('lst' in data['href']) :
    		fileurl=data['href']

    r3 = requests.get(fileurl, allow_redirects=True)
    open('./static/textfiles/temp.txt', 'wb').write(r3.content)

    #%% Calculating velocity

    obs = np.loadtxt('./static/textfiles/temp.txt')
    v_obs = obs[:, 9]           #remove unwanted velocities
    
    return v_obs

 
app = flask.Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    address="http://127.0.0.1:5000/"

else:
    app.debug = False
    address="https://spacewapi.herokuapp.com/" 


@app.route('/', methods=['GET'])
def home():
    x = str(request.args['text'])
    cr=convert(x)
    if (not os.path.exists("./static/images/inp_"+str(cr)+".png")):
        ret=get_input(int(cr))
    ret="success"
    try:
        if ret=="success":
            response = flask.jsonify({
                "cr_number" : cr,
                "plot" : "Brrss",
                "message" : "the graphs you requested can be found at the following urls",
                "input_map":address+"getplot/?graph=inp_"+str(cr),
                "solar_surface_map":address+"getplot/?graph=outp_"+str(cr),
                #"solar_surface_magnetic_field":address+"getplot/?graph=Brrss_"+str(cr),
                "velocity_at_1AU":address+"getplot/?graph=velprofile_"+str(cr),
                "fieldlines":address+"getplot/?graph=fieldlines_"+str(cr),
                "comparison":address+"getplot/?graph=comparison_"+str(cr),
                "vel_with_r":address+"getplot/?graph=velwithr_"+str(cr),
             })

    # Enable Access-Control-Allow-Origin
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
           return flask.jsonify({
               "cr number": cr,
               "message":"there was an error in processing your request"})
           
    except KeyError:
        return 'bye'
    
@app.route('/velocity/', methods=['GET'])
def velocity():
    x = str(request.args['text'])
    date=get_date(x)
    y=str(date)
    y=y[:4]+y[5:7]+y[8:10]
    v_obs= get_vel(y)
    avg_vel=sum(v_obs) / len(v_obs)
    max_vel=max(v_obs)
    min_vel=min(v_obs)
    try:
        if avg_vel:
            response = flask.jsonify({
                "avg_vel" : avg_vel,
                "min_vel" : min_vel,
                "max_vel" : max_vel
             })
    # Enable Access-Control-Allow-Origin
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
           return flask.jsonify({
               "date": date,
               "message":"there was an error in processing your request"})
           
    except KeyError:
        return 'bye'

@app.route('/velocity_plot/', methods=['GET'])
def velocity_plot():
    x = str(request.args['text'])
    date=get_date(x)
    y=str(date)
    y=y[:4]+y[5:7]+y[8:10]
    v_obs= get_vel(y).tolist()
    try:
        if v_obs[0]:
            response = flask.jsonify({
                "velocity" : v_obs, 
                "success" : True
                })
    # Enable Access-Control-Allow-Origin
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
           return flask.jsonify({
               "date": date,
               "message":"there was an error in processing your request"})
           
    except KeyError:
        return 'bye'

@app.route("/avgvelocity/")
def avgvel():
    x = str(request.args['text'])
    date=get_date(x)
    y=str(date)
    y=y[:4]+y[5:7]+y[8:10]
    v_obs= get_vel(y)
    avg_vel=sum(v_obs) / len(v_obs)
    months=["January","February","March","April","May","June","July","August","September","October","November","December"]
    spokendate=str(int(y[6:]))+"+"+months[int(y[4:6])-1]+"+"+y[:4]
    return flask.jsonify({
        "param":"average velocity",
        "date" : spokendate,
        "val":str(round(avg_vel,2))+"km/s",
        "url":address+"get_audio/?date="+spokendate+"&params=average+velocity&val="+str(round(avg_vel,2))+"+kilometers+per+second.",
        })
    

@app.route("/get_audio/")
def streamwav():
    date=str(request.args["date"])
    param=str(request.args["params"])
    val=str(request.args["val"])
    mytext = 'The '+param+' on '+date+" is : "+val
    print(mytext)
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("./static/audio/welcome.mp3")
    def generate():
        with open("./static/audio/welcome.mp3", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return flask.Response(generate(), mimetype="audio/mp3")

@app.route('/getplot/',methods=['GET'])
def getplot():
    loc=str(request.args['graph']).split("_")
    cr=loc[1]
    plot=loc[0]
    url="./static/images/"+str(plot)+"_"+str(cr)+".png"
    try:
        if url:
            return flask.send_file(url, mimetype='image/png')
        else:
            return flask.jsonify(
                {"cr number" : cr,
                 "plot" : plot,
                 "message" : "the graph you requested has either not been computed or doesn't exist"})
    except KeyError:
        return 'bye'

if __name__=='__main__':
    app.run()