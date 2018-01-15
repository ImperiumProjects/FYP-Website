from urllib2 import urlopen
from bs4 import BeautifulSoup

import mysql.connector
from mysql.connector import errorcode

# specify the url
info_page = "https://www.met.ie/default.asp?LW=Cork"

page = urlopen(info_page)
soup = BeautifulSoup(page, "html.parser")

name_box = soup.find("table", {"class": "quickinfotext"})
value_fields = name_box.findAll("td")

print(value_fields[5])

#for output in value_fields:
#    print(output)
"""
value_output = value_fields[0].text.strip()
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
"""

#
# MySQL Database Connection
#

"""
config = {
    'user': 'scraper',
    'password': 'scraper',
    'host': '84.200.193.29',
    'database': 'historical'
}
"""