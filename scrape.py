# import libraries

#import urllib2
from urllib.request import urlopen

from bs4 import BeautifulSoup

# specify the url

info_page = "https://www.tidetimes.org.uk/cork-city-tide-times"

page = urlopen(info_page)

soup = BeautifulSoup(page, "html.parser")

name_box = soup.find("table", {"id": "tidetimes"})

fields = name_box.findAll("td", {"class" : "tar"})

#name = name_box.text.strip()
print(fields[1].text.strip())