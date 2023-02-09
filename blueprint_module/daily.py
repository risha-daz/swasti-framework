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

AVG_VEL="""SELECT
ROUND(AVG(temperature),2) as temp_avg, ROUND(AVG(speed),2) as vel_avg, ROUND(CAST(AVG(density) as numeric),2) as dens_avg
FROM obsdata
WHERE  timestamp < %s::date
AND    timestamp   >= %s::date;"""

@blueprint.route('/get_obs',methods=['GET'])
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


@blueprint.route("/avgvelocity/")
def avgvel():
    x = str(request.args['text'])
    date=get_date(x)
    y=str(date)
    y=y[:4]+y[5:7]+y[8:10]
    end_date=date + dt.timedelta(days=1)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(AVG_VEL, (end_date, date))
            average = cursor.fetchall()
    print(average)
    avg_vel=average[0][1]
    avg_temp=average[0][0]
    avg_den=average[0][2]
    months=["January","February","March","April","May","June","July","August","September","October","November","December"]
    spokendate=str(int(y[6:]))+"+"+months[int(y[4:6])-1]+"+"+y[:4]
    response=flask.jsonify({
        "date": spokendate,
        "val" : str(avg_vel) + " km/s",
        "avg_temp": avg_temp,
        "avg_den" : avg_den,
        "url" : address + "get_audio/?date=" + spokendate + "&params=average+velocity&val=" + str(avg_vel) + "+kilometers+per+second.",
        })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    