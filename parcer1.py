from urllib import request
from bs4 import BeautifulSoup
import json

url = 'http://newsline.kg/getNews.php?limit=30&last_dt=2022-07-04%2007:57:33.933739'

html = request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
site_json = json.loads(soup.text)


data = site_json['data']

with open('Новости.json', 'w') as file:
    json.dump(data, file, indent=2)


with open('Новости.json', 'r') as file:
    data = file.read()

print(data)
