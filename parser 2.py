import itertools
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


url = 'https://www.akchabar.kg/ru/exchange-rates/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


def write_csv(data: list, field_names, file_name):
    # function to save in csv file
    with open(file_name, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(field_names)
        for row in data:
            writer.writerow(row)


currency_table = soup.find('table', class_='tablesorter table-hover hidden-xs')  # getting whole table
rows = currency_table.find('tbody').find_all('tr')  # getting all the prices of currencies
currencies = currency_table.find('thead').find_all('th')  # getting all the names of currencies

price_list = []  # list for prices of currencies
name_currency_list = []  # list for names of currencies

for curr in currencies:
    name_currency_list += [curr.text]


for row in rows:
    """
    process of validation
    from str to int 
    """
    price_list += [[
        float(item.text.replace(',', '.')) if index != 0 else item.text
        for index, item in enumerate(row.find_all('td'))
    ]]

name_currency_list = [
    #  dividing currencies into two categories example: [usd buy, usd sell]
    [f'{item} buy', f'{item} sell'] if index != 0 else [item]
    for index, item in enumerate(name_currency_list)

]
#  print(name_currency_list)

name_currency_list = list(itertools.chain(*name_currency_list))  # making one-dimensional list

file_name = soup.find('div', class_='col-md-8 col-xs-12').text.split(',')[1] + '.csv'  # defining an update date


print(file_name) # file_name
write_csv(price_list, name_currency_list, file_name=file_name.strip())  # finally saving in csv file :)


