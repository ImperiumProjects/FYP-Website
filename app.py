#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file
import pymysql
import app_prediction
import php_python

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/test')
def test_script():
    db = pymysql.connect(host="84.200.193.29",
                     port=3306,
                     user="scraper",
                     passwd="scraper",
                     db="historical")
    app_prediction.predict()
    cur = db.cursor()
    cur.execute("SELECT percentage FROM predictions ORDER BY id DESC LIMIT 1")
    sql_percent = str(cur.fetchone())[1:-2]
    percent = {"percent": sql_percent}
    cur.close()
    return '''
<html>
    <head>
        <title>Leeway Predictions</title>
        <link rel="icon" href="leeway_logo.png">
    </head>
    <body>
        P: ''' + percent['percent'] + '''
    </body>
</html>'''

@app.route('/forecasts')
def prediction_script():
    db = pymysql.connect(host="84.200.193.29",
                     port=3306,
                     user="scraper",
                     passwd="scraper",
                     db="historical")
    cur = db.cursor()
    cur.execute("SELECT level FROM two_point_data ORDER BY id DESC LIMIT 1")
    sql_riverlevel = str(cur.fetchone())[10:-4]
    riverlevel = {"riverlevel" : sql_riverlevel}
    cur.execute("SELECT degrees FROM weather ORDER BY id DESC LIMIT 1")
    sql_templevel = str(cur.fetchone())[1:-2]
    templevel = {"templevel": sql_templevel}
    cur.execute("SELECT level FROM tidal ORDER BY id DESC LIMIT 1")
    sql_tidallevel = str(cur.fetchone())[10:-4]
    tidallevel = {"tidallevel": sql_tidallevel}
    cur.execute("SELECT percentage FROM predictions ORDER BY id DESC LIMIT 1")
    sql_percent = str(cur.fetchone())[1:-2]
    percent = {"percent": sql_percent}

    cur.execute("SELECT prediction FROM seven_day_forecast ORDER BY id DESC LIMIT 1")
    sql_sevenday = str(cur.fetchone())[1:-2]
    sevenday = {"sevenday": sql_sevenday}

    cur.execute("SELECT prediction FROM two_week_forecast ORDER BY id DESC LIMIT 1")
    sql_twoweek = str(cur.fetchone())[1:-2]
    twoweek = {"twoweek": sql_twoweek}

    cur.execute("SELECT prediction FROM one_month_forecast ORDER BY id DESC LIMIT 1")
    sql_onemonth = str(cur.fetchone())[1:-2]
    onemonth = {"onemonth": sql_onemonth}
    cur.close()
    return '''
<html>
    <head>
        <title>Leeway Forecasts</title>
        <link rel="icon" href="leeway_logo.png">
    </head>
    <body>
        River: ''' + riverlevel['riverlevel'] + '''<br>
        Temp: ''' + templevel['templevel'] + '''<br>
        Tidal: ''' + tidallevel['tidallevel'] + '''<br>
        Rain: ''' + percent['percent'] + '''<br>
        Seven: ''' + sevenday['sevenday'] + '''<br>
        Two: ''' + twoweek['twoweek'] + '''<br>
        One: ''' + onemonth['onemonth'] + '''
    </body>
</html>'''

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/leeway_logo.png')
def get_logo_image():
    return send_file('leeway_logo.png', mimetype='image/png')

@app.route('/website_background_river.png')
def get_background_image():
    return send_file('website_background_river.png', mimetype='image/png')

@app.route('/website_background_opposite.png')
def get_opposite_image():
    return send_file('website_background_opposite.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
