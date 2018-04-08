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

print(first_high_tide_time)
print(first_high_tide_height)

print(second_low_tide_time)
print(second_low_tide_height)