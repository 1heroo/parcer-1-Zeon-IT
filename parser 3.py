import requests
from bs4 import BeautifulSoup as Bs
import csv
import pandas as pd
#  from fake_useragent import UserAgent


site_url = "https://ru.wikipedia.org/"
url = "https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%9A%D0%B8%D1%80%D0%B3%D0%B8%D0%B7%D0%B8%D0%B8"
response = requests.get(url)
soup = Bs(response.text, 'lxml')


cities_table = soup.find('table', class_="wikitable sortable")  # extracting whole table of cities
table_header = cities_table.find_all('th')  # extracting column names as tags
table_body = cities_table.find_all('td')  # extracting values as tags

columns_amount = len(table_header)  # len of columns
fields_amount = len(table_body)  # total amount of all values

list_headers = [item.text.replace('\n', '') for item in table_header]  # extracting and validating text from tags
list_body = [item.text for item in table_body]  # extracting text from tags
#  print(list_headers)

list_urls = []
for i in range(0, fields_amount, columns_amount):
    # extracting urls from names of the cities
    list_urls += [site_url + table_body[i].find('a').get('href')]
list_urls = pd.Series(list_urls)  # converting them into pd.Series to add in table


list_raws = []
for _ in range(int(fields_amount / columns_amount)):
    # dynamic algorythm to fold all the values into list of lists
    # it will work even if we add some new columns in initial table
    holder = []
    for _ in range(columns_amount):
        holder += [list_body.pop(0).replace('\n', ' ')]
    list_raws += [holder]
    holder = []


def write_csv(data: list, field_names, file_name):
    # function to save in csv file
    with open(file_name, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(field_names)
        for row in data:
            writer.writerow(row)


file_name = 'kg_cities.csv'

write_csv(list_raws, list_headers, file_name)


"""
one of the easiest ways to add new columns in table is pandas way 

here you go
"""

df = pd.read_csv(file_name)  # reading the csv file
df['Ссылки на страницу городов'] = list_urls  # adding new columns of urls
# print(df.columns)
df.to_csv(file_name)  # saving again :)
