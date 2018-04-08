from urllib2 import urlopen
from bs4 import BeautifulSoup

import json

import time

import mysql.connector
from mysql.connector import errorcode

"""
Info being scraped from: http://data.corkcity.ie/dataset/51982a53-4543-40c1-9c2d-de801ee60b6e/resource/1ff23e53-a0ab-4dc8-95e3-31a669547a80/view/0ff0c9b1-2d59-4542-9f9f-94b8f5e40922
"""

url = 'http://data.corkcity.ie/api/action/datastore_search?resource_id=1ff23e53-a0ab-4dc8-95e3-31a669547a80&limit=2'
fileobj = urlopen(url)
output = fileobj.read()
json_encode = json.loads(output)

config = {
    'user': 'scraper',
    'password': 'scraper',
    'host': '84.200.193.29',
    'database': 'historical'
}

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    add_first_riverLevel = ("""INSERT INTO two_point_data
    							(level, latitude, longitude)
    							VALUES (%s, %s, %s) """)
    data_first_riverLevel = (json_encode['result']['records'][0]['level'], json_encode['result']['records'][0]['latitude'], json_encode['result']['records'][0]['longitude'])
    cursor.execute(add_first_riverLevel, data_first_riverLevel)

    add_second_riverLevel = ("""INSERT INTO two_point_data
    							(level, latitude, longitude)
    							VALUES (%s, %s, %s) """)
    data_second_riverLevel = (json_encode['result']['records'][1]['level'], json_encode['result']['records'][1]['latitude'], json_encode['result']['records'][1]['longitude'])
    cursor.execute(add_second_riverLevel, data_second_riverLevel)

    cnx.commit()

    cursor.close()
    cnx.close()  

except mysql.connector.Error as e:
    try:
        print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
    except IndexError:
        print ("MySQL Error: %s" % str(e))