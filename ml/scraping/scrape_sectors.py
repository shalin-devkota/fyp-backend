from bs4 import BeautifulSoup as bs
import requests
import os
import json

url = "https://merolagani.com/CompanyList.aspx"

response = requests.get(url)
soup = bs(response.text, 'html.parser')

sectors = {}

panels = soup.find_all("div", class_="panel panel-default")

for panel in panels:
    sector_name = panel.find("h3", class_="panel-title").find("a").text.strip()
    stock_symbols = []
    
    collapse_div = panel.find('div', class_='panel-collapse')

    
    if collapse_div:
        table_div = collapse_div.find("div", class_="table-responsive")

        if table_div:
            table = table_div.find("table")

            if table:
                rows = table.find_all("tr")[1:]

            for row in rows:
                stock_symbol = row.find('td', class_='text-left').find('a').text.strip()
                stock_symbols.append(stock_symbol)

            sectors[sector_name] = stock_symbols
    
print(sectors)

json_file_path = os.path.join("..", "data", "sectors.json")
with open(json_file_path, "w") as json_file:
    json.dump(sectors, json_file, indent=4)

print(f"Scraping completed and saved to {json_file_path}")
