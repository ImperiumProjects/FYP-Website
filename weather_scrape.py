from urllib2 import urlopen
from bs4 import BeautifulSoup

import time

import mysql.connector
from mysql.connector import errorcode

"""
Info being scraped from: https://www.met.ie/default.asp?LW=Cork
"""

# specify the url
info_page = "https://www.met.ie/default.asp?LW=Cork"

page = urlopen(info_page)
soup = BeautifulSoup(page, "html.parser")

name_box = soup.find("table", {"class": "quickinfotext"})
value_fields = name_box.findAll("td")

output = value_fields[5]
current_degrees = (str(output)[35])

config = {
    'user': 'scraper',
    'password': 'scraper',
    'host': '84.200.193.29',
    'database': 'historical'
}

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    add_temp = ("""INSERT INTO weather
                        (degrees, time)
                        VALUES (%s, %s) """)
    data = (current_degrees, time.strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute(add_temp, data)

    cnx.commit()

    cursor.close()
    cnx.close()
except mysql.connector.Error as e:
    try:
        print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
    except IndexError:
        print ("MySQL Error: %s" % str(e))