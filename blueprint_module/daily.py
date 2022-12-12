from . import blueprint
import psycopg2
import flask
from flask import request, jsonify
import datetime as dt
from datetime import datetime
from dateutil import parser
from dotenv import load_dotenv
import numpy as np
import html5lib
#import sunpy.map
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

import os

def get_date(x):
    return parser.parse(x, fuzzy=True)

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

ENV = 'prod'

if ENV == 'dev':
    address="http://127.0.0.1:5000/"
else:
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

@blueprint.route('/get_obs',methods=['GET'])
def obs_temp():
    x = str(request.args['param'])
    date=get_date(x)
    end_date=date + dt.timedelta(days=1)
    end_week=date + dt.timedelta(days=8)
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


@blueprint.route("/avgvelocity/")
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
    