from urllib2 import urlopen
from bs4 import BeautifulSoup

import mysql.connector
from mysql.connector import errorcode

# specify the url
info_page = "https://www.tidetimes.org.uk/cork-city-tide-times"

page = urlopen(info_page)
soup = BeautifulSoup(page, "html.parser")

name_box = soup.find("table", {"id": "tidetimes"})
value_fields = name_box.findAll("td", {"class" : "tar"})

time_fields = name_box.findAll("td", {"class" : "tac"})

value_output = value_fields[1].text.strip()
first_high_tide_height = value_output[1:-2]

time_output = time_fields[2].text.strip()
first_high_tide_time = time_output

value_output = value_fields[2].text.strip()
time_output = time_fields[3].text.strip()

first_low_tide_height = value_output[1:-2]
first_low_tide_time = time_output

value_output = value_fields[3].text.strip()
time_output = time_fields[4].text.strip()

second_high_tide_height = value_output[1:-2]
second_high_tide_time = time_output

value_output = value_fields[4].text.strip()
time_output = time_fields[5].text.strip()

second_low_tide_height = value_output[1:-2]
second_low_tide_time = time_output

#
# MySQL Database Connection
#

config = {
    'user': 'scraper',
    'password': 'scraper',
    'host': '84.200.193.29',
    'database': 'historical'
}

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    add_first_high = ("""INSERT INTO tidal
                        (tide, time, level)
                        VALUES (%s, %s, %s) """)
    data_first_high = ("high", first_high_tide_time, first_high_tide_height)
    cursor.execute(add_first_high, data_first_high)

    add_first_low = ("""INSERT INTO tidal
                        (tide, time, level)
                        VALUES (%s, %s, %s) """)
    data_first_low = ("low", first_low_tide_time, first_low_tide_height)
    cursor.execute(add_first_low, data_first_low)

    add_second_high = ("""INSERT INTO tidal
                        (tide, time, level)
                        VALUES (%s, %s, %s) """)
    data_second_high = ("high", second_high_tide_time, second_high_tide_height)
    cursor.execute(add_second_high, data_second_high)

    add_second_low = ("""INSERT INTO tidal
                        (tide, time, level)
                        VALUES (%s, %s, %s) """)
    data_second_low = ("low", second_low_tide_time, second_low_tide_height)
    cursor.execute(add_second_low, data_second_low)

    cnx.commit()

    cursor.close()
    cnx.close()
except mysql.connector.Error as e:
    try:
        print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
    except IndexError:
        print ("MySQL Error: %s" % str(e))