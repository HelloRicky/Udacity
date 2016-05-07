import json
import requests
from bs4 import BeautifulSoup

url = "http://www.transtats.bts.gov/Data_Elements.aspx?Data=2"

s = requests.Session()
r = s.get(url)
soup = BeautifulSoup(r.text, "html.parser")
viewstate_element = soup.find(id = "__VIEWSTATE")
viewstate = viewstate_element["value"]
eventvalidation_element = soup.find(id = "__EVENTVALIDATION")
eventvalidation = eventvalidation_element["value"]

r = requests.post(url, data = {
            'AirportList': "BOS",
            'CarrierList': "VX",
            'Submit': 'Submit',
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__EVENTVALIDATION": eventvalidation,
            "__VIEWSTATE": viewstate
        })
f = open("airport_w.html", "w")
f.write(r.text)
print "end"