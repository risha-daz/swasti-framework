from . import blueprint
import psycopg2
import flask
from flask import request, jsonify
import datetime as dt
from datetime import datetime
from dateutil import parser
from dotenv import load_dotenv
import os

load_dotenv()
url= os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

def get_date(x):
    return parser.parse(x, fuzzy=True)

WEEKLY_DATA=HOURLY_DATA="""SELECT
  date_trunc('day', timestamp) as timestamp, 
  ROUND(AVG(temperature),2) as temp_avg, ROUND(AVG(speed),2) as vel_avg, ROUND(CAST(AVG(density) as numeric),2) as dens_avg
FROM obsdata
WHERE  timestamp < %s::date
AND    timestamp   >= %s::date
GROUP BY 1 ORDER BY timestamp;"""

@blueprint.route('/weekly',methods=['GET'])
def weekly():
    x = str(request.args['param'])
    date=get_date(x)
    end_date=date + dt.timedelta(days=7)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(WEEKLY_DATA, (end_date, date))
            average = cursor.fetchall()
    response=flask.jsonify({"data":average})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
