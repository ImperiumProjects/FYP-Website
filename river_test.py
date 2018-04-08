from bs4 import BeautifulSoup
from selenium import webdriver

import time

url = "http://data.corkcity.ie/dataset/51982a53-4543-40c1-9c2d-de801ee60b6e/resource/1ff23e53-a0ab-4dc8-95e3-31a669547a80/view/0ff0c9b1-2d59-4542-9f9f-94b8f5e40922"
browser = webdriver.PhantomJS()
browser.get(url)
time.sleep(5)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
a = soup.find('div', {'class': 'leaflet-popup-content'})

print(a)