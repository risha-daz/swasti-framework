from flask import Flask, render_template, request
from sunpy.coordinates import sun

from datetime import datetime
from dateutil import parser

app=Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

@app.route('/')
def index():
    return render_template('index.html')

def convert(x):
    y=0
    try:
        y=parser.parse(x, fuzzy=True)
    except:
        if("now" in x or "today" in x):
            y=datetime.now()
        else:
            return "not a date"

    if y:
        return sun.carrington_rotation_number(y)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method=='POST':
        final_text = request.form['mytext']
    # response = jsonify({'some': str(convert(final_text))})
    try:
        y=parser.parse(final_text, fuzzy=True)
    except:
        if("now" in final_text or "today" in final_text):
            y=datetime.now().date()
        else:
            y="date not understood"

    return render_template('index.html', message={"heard": y.date(), "ans": convert(final_text)})

if __name__=='__main__':
    app.run()