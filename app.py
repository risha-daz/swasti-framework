#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 06:26:15 2022

@author: sdas
"""

import flask
from flask import request, jsonify
import datetime as dt
from datetime import datetime
from dateutil import parser

#from sunpy.coordinates import sun
import math
from gtts import gTTS

#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt

import numpy as np
import html5lib
#import sunpy.map
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

import os
import psycopg2

def get_date(x):
    return parser.parse(x, fuzzy=True)

# def convert(x):
#     y=0
#     try:
#         y=get_date(x)
#     except:
#         if("now" in x or "today" in x):
#             y=datetime.now()
#         else:
#             print("date not understood")

#     if y:
#         return math.floor(sun.carrington_rotation_number(y))
#     else:
#         return 0




#%% Enter the CR and magnetogram

# def get_input(cr):
    
#     URL = "https://gong.nso.edu/data/magmap/crmap.html"
#     r = requests.get(URL)
    
#     #cr = 2053           # Carrignton rotation number
#     mag = 'GONG'        # Magnetogram type (GONG/HMI)

#     soup = BeautifulSoup(r.content, 'html5lib')
#     fileurl=''
#     alla=soup.find_all("a", href=True)
#     data = '' 
#     for data in alla:
#     	if(str(cr) in data['href']) :
#             fileurl="https://gong.nso.edu"+data['href']
    
#     gong_map = sunpy.map.Map(fileurl)


#     # transforming fits file into sunpy map
#     input_map = sunpy.map.Map(gong_map.data- np.mean(gong_map.data), gong_map.meta)

#     #%% Define pfsspy Grid

#     nrho = 100
#     rss = 2.50                      #Setting source surface (ss) = 2.50 Rsun

#     #%% Solving PFSS model to get the Output at source surface

#     input = pfsspy.Input(input_map, nrho, rss)
#     output = pfsspy.pfss(input)


#     # Input map at 1.0 R
#     m = input.map
#     fig = plt.figure()
#     ax = plt.subplot(projection=m)
#     m.plot(vmax=-50, vmin =50)
#     plt.colorbar()
#     ax.set_title('Input field')
#     plt.savefig("./static/images/inp_"+str(cr)+".png")
#     plt.close()
#     # Output map at 2.5 R
#     ss_br = output.source_surface_br
#     fig = plt.figure()
#     ax = plt.subplot(projection=ss_br)

#     ss_br.plot()
#     # Plot the polarity inversion line (i.e. where B changes its sign or where B=0)
#     ax.plot_coord(output.source_surface_pils[0])

#     plt.colorbar()
#     ax.set_title('Source surface magnetic field')
#     plt.savefig("./static/images/outp_"+str(cr)+".png")
#     plt.close()
    
#     if (m):
#         return "success"
#     else:
#         return "fail"

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

    # Calculating velocity

    obs = np.loadtxt('./static/textfiles/temp.txt')
    v_obs = obs[:, 9]           #remove unwanted velocities
    t_obs= obs[:, 7]
    d_obs=obs[:, 8]
    return v_obs, t_obs, d_obs

 
app = flask.Flask(__name__,static_url_path='/',static_folder='./client/build')

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    address="http://127.0.0.1:5000/"

else:
    app.debug = False
    address="https://swasti-framework.azurewebsites.net/" 

load_dotenv()
url= os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

end_date = dt.date(2022,1,5) #datetime.now()+ dt.timedelta(days=1)
start_date = dt.date(2022,1,4) #datetime.now()

HOURLY_DATA="""SELECT * from obsdata
WHERE  timestamp < %s::date
AND    timestamp   >= %s::date 
order by timestamp;"""
#print(HOURLY_DATA)
CALC_DATA="""SELECT speed from calcdata
WHERE  timestamp < %s::date
AND    timestamp   >= %s::date 
order by timestamp;"""

@app.route('/',methods=['GET'])
def index():
    return app.send_static_file('index.html')

# @app.route('/quer/', methods=['GET'])
# def home():
#     x = str(request.args['text'])
#     cr=convert(x)
#     if (not os.path.exists("./static/images/inp_"+str(cr)+".png")):
#         ret=get_input(int(cr))
#     ret="success"
#     try:
#         if ret=="success":
#             response = flask.jsonify({
#                 "cr_number" : cr,
#                 "plot" : "Brrss",
#                 "message" : "the graphs you requested can be found at the following urls",
#                 "input_map":address+"getplot/?graph=inp_"+str(cr),
#                 "solar_surface_map":address+"getplot/?graph=outp_"+str(cr),
#                 #"solar_surface_magnetic_field":address+"getplot/?graph=Brrss_"+str(cr),
#                 "velocity_at_1AU":address+"getplot/?graph=velprofile_"+str(cr),
#                 "fieldlines":address+"getplot/?graph=fieldlines_"+str(cr),
#                 "comparison":address+"getplot/?graph=comparison_"+str(cr),
#                 "vel_with_r":address+"getplot/?graph=velwithr_"+str(cr),
#              })

#     # Enable Access-Control-Allow-Origin
#             response.headers.add("Access-Control-Allow-Origin", "*")
#             return response
#         else:
#            return flask.jsonify({
#                "cr number": cr,
#                "message":"there was an error in processing your request"})
           
#     except KeyError:
#         return 'bye'
    
# @app.route('/velocity/', methods=['GET'])
# def velocity():
#     x = str(request.args['text'])
#     date=get_date(x)
#     y=str(date)
#     y=y[:4]+y[5:7]+y[8:10]
#     v_obs, t_obs, d_obs= get_vel(y)
#     avg_vel=sum(v_obs) / len(v_obs)
#     max_vel=max(v_obs)
#     min_vel=min(v_obs)
#     avg_temp=sum(t_obs) / len(t_obs)
#     max_temp=max(t_obs)
#     min_temp=min(t_obs)
#     avg_den=sum(d_obs) / len(d_obs)
#     max_den=max(d_obs)
#     min_den=min(d_obs)
#     try:
#         if avg_vel:
#             response = flask.jsonify({
#                 "avg_vel" : avg_vel,
#                 "min_vel" : min_vel,
#                 "max_vel" : max_vel,
#                 "avg_temp" : avg_temp,
#                 "min_temp" : min_temp,
#                 "max_temp" : max_temp,
#                 "avg_den" : avg_den,
#                 "min_den" : min_den,
#                 "max_den" : max_den

#              })
#     # Enable Access-Control-Allow-Origin
#             response.headers.add("Access-Control-Allow-Origin", "*")
#             return response
#         else:
#            return flask.jsonify({
#                "date": date,
#                "message":"there was an error in processing your request"})
           
#     except KeyError:
#         return 'bye'

@app.route('/get_obs',methods=['GET'])
def obs_temp():
    x = str(request.args['param'])
    date=get_date(x)
    end_date=date + dt.timedelta(days=1)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(HOURLY_DATA, (end_date, date))
            average = cursor.fetchall()
    vel=[]
    tmp=[]
    dens=[]
    for i in range(len(average)):
        vel.append(average[i][6])
        tmp.append(average[i][4])
        dens.append(average[i][5])
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CALC_DATA, (end_date, date))
            average = cursor.fetchall()
    calcvel=[]
    for i in range(len(average)):
        calcvel.append(average[i][0])
    response=flask.jsonify({"velocity" : vel, "density": dens, "temp" : tmp, "calcvel":calcvel
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# @app.route('/velocity_plot/', methods=['GET'])
# def velocity_plot():
#     x = str(request.args['text'])
#     date=get_date(x)
#     y=str(date)
#     y=y[:4]+y[5:7]+y[8:10]
#     v_obs= get_vel(y).tolist()
#     try:
#         if v_obs[0]:
#             response = flask.jsonify({
#                 "velocity" : v_obs, 
#                 "success" : True
#                 })
#     # Enable Access-Control-Allow-Origin
#             response.headers.add("Access-Control-Allow-Origin", "*")
#             return response
#         else:
#            return flask.jsonify({
#                "date": date,
#                "message":"there was an error in processing your request"})
           
#     except KeyError:
#         return 'bye'

@app.route("/avgvelocity/")
def avgvel():
    x = str(request.args['text'])
    date=get_date(x)
    y=str(date)
    y=y[:4]+y[5:7]+y[8:10]
    v_obs, t_obs, d_obs= get_vel(y)
    avg_vel=sum(v_obs) / len(v_obs)
    avg_temp=sum(t_obs) / len(t_obs)
    avg_den=sum(d_obs) / len(d_obs)
    months=["January","February","March","April","May","June","July","August","September","October","November","December"]
    spokendate=str(int(y[6:]))+"+"+months[int(y[4:6])-1]+"+"+y[:4]
    response=flask.jsonify({
 
        "date" : spokendate,
        "val":str(round(avg_vel,2))+"km/s",
        "avg_temp":avg_temp,
        "avg_den": avg_den,
        "url":address+"get_audio/?date="+spokendate+"&params=average+velocity&val="+str(round(avg_vel,2))+"+kilometers+per+second.",
        })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    

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

# @app.route('/getplot/',methods=['GET'])
# def getplot():
#     loc=str(request.args['graph']).split("_")
#     cr=loc[1]
#     plot=loc[0]
#     url="./static/images/"+str(plot)+"_"+str(cr)+".png"
#     try:
#         if url:
#             return flask.send_file(url, mimetype='image/png')
#         else:
#             return flask.jsonify(
#                 {"cr number" : cr,
#                  "plot" : plot,
#                  "message" : "the graph you requested has either not been computed or doesn't exist"})
#     except KeyError:
#         return 'bye'

if __name__=='__main__':
    app.run()

# %%
