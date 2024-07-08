import requests
from bs4 import BeautifulSoup
import random
import json
import re

#First Page To Scrape
url = "https://docs.stellarcyber.ai/prod-docs/5.1.x/Using/ML/Machine-Learning-by-xdr-event-name.htm"


session = requests.session()
ua_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577"
,"Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36"
,"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36", "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
,"Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]


ua = random.choice(ua_list)
headers = {'User-Agent': ua}
request = session.get(url, headers=headers)
content = request.text

soup = BeautifulSoup(content, 'html.parser')
tables = soup.find_all('table')


table = soup.find('table', class_='TableStyle-simple-border')

data_out = {}

for row in table.tbody.find_all('tr', class_='TableStyle-simple-border-Body-Body1'):
    columns = row.find_all('td')
    alert_name = columns[0].find('p').get_text()
    
    list_items = columns[1].find_all('li')
    
    key_fields_list = []
    
    for i in list_items:
        if "</code> — " in str(i):
            field_no_split = i.get_text()
            field_split = field_no_split.split(" — ")
          
            field_json = {
                "description": field_split[1].strip(),
                "name": field_split[0].strip()
                }
            key_fields_list.append(field_json)

    
    data = {
        alert_name: {
                "key_fields": key_fields_list
            }
        }
    data_out.update(data)



#Second Page To Scrape
url = "https://docs.stellarcyber.ai/prod-docs/5.1.x/Using/Alerts/Alert-Key-Fields.htm?tocpath=REFERENCE|Detection%20and%20Correlation%20Overview|_____4"

session = requests.session()
ua_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577"
,"Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36"
,"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36", "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
,"Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]

ua = random.choice(ua_list)
headers = {'User-Agent': ua}
request = session.get(url, headers=headers)
content = request.text

soup = BeautifulSoup(content, 'html.parser')
tables = soup.find_all('table')
table = soup.find('table', class_='TableStyle-TableStyles')

regex = re.compile('TableStyle-TableStyles-Body-Body.*')

for row2 in table.find_all('tr', class_=regex):
    columns2 = row2.find_all('td')
    first_column = columns2[0]
    display_names = first_column.find_all('p')
    event_name = display_names[1].get_text().strip('(',).strip(')')

    grouping = row2.find_all('tr')

    key_fields_third_party = []
    for x in grouping:
        testing2 = x.find_all('td')
        key_field2 = testing2[0].get_text()
        display_name = testing2[1].get_text()

        field_json = {
                "description": display_name,
                "name": key_field2
                }
        key_fields_third_party.append(field_json)

    data = {
        event_name: {
                "key_fields": key_fields_third_party
            }
        }
    data_out.update(data)


print(json.dumps(data_out))
