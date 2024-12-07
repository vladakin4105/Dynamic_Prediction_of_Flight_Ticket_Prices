import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

url = "https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Romania"
page = requests.get(url)
soup = bs(page.text, 'html.parser')

table = soup.find_all('table')[2]
table_titles = table.find_all('th')
city_table_titles = [title.text.strip() for title in table_titles]

df = pd.DataFrame(columns = city_table_titles)

table_content = table.tbody.find_all("tr")[1:]
for row in table_content:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]
    if len(individual_row_data) == len(city_table_titles):
            df.loc[len(df)] = individual_row_data

df.to_csv(r"cities.csv", index = False)