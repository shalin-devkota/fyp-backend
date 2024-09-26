from bs4 import BeautifulSoup as soup
import requests
from stock.models import Stock
from django.core.management.base import BaseCommand
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
import random
import json
import os

"""
SITES LEFT TO SCRAPE FROM:
1)NEPALI PAISA (API)

"""

with open("sectors.json", "r") as json_file:
    sectors = json.load(json_file)

stock_sector_map = dict()

for sector, symbols in sectors.items():
    for symbol in symbols:
        stock_sector_map[symbol] = sector
    

class Command(BaseCommand):
    help = "fix the description images"

    def safe_decimal(self,value):
        try:
            return Decimal(value.replace(",", ""))
        except InvalidOperation:
            return None

   
    def safe_int(self,value):
        try:
            return int(float(value.replace(",", "")))
        except ValueError:
            return None


    def sharesansar_scraper(self):
        stocks = []
        base_url = "https://www.sharesansar.com/live-trading"

        data_html = requests.get(base_url)
        data_soup = soup(data_html.text, "html.parser")

        table = data_soup.find("table", {"id": "headFixed"})

        # Define the order of the fields
        field_names = [
            "id",
            "symbol",
            "ltp",
            "point_change",
            "percentage_change",
            "open",
            "high",
            "low",
            "volume",
            "prev_close",
        ]

        for row in table.find_all("tr")[1:]:  # Skip the header row
            cells = row.find_all("td")
            if len(cells) == len(field_names):  # Ensure there are enough cells
                stock_data = {
                    field: cells[i].text.strip() for i, field in enumerate(field_names)
                }

                # Function to safely convert to Decimal
                

                try:
                    Stock.objects.update_or_create(
                        symbol=stock_data["symbol"],
                        defaults={
                            "ltp": self.safe_decimal(stock_data["ltp"]),
                            "point_change": self.safe_decimal(stock_data["point_change"]),
                            "percentage_change": self.safe_decimal(
                                stock_data["percentage_change"]
                            ),
                            "open_price": self.safe_decimal(stock_data["open"]),
                            "high_price": self.safe_decimal(stock_data["high"]),
                            "low_price": self.safe_decimal(stock_data["low"]),
                            "volume": self.safe_int(stock_data["volume"]),
                            "prev_close": self.safe_decimal(stock_data["prev_close"]),
                            "sector": stock_sector_map.get(stock_data["symbol"], "N/A"),
                        },
                    )
                    stocks.append(stock_data)
                except ValidationError as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error processing stock {stock_data['symbol']}: {str(e)}"
                        )
                    )

    def chukul_scraper(self):
        base_url = 'https://chukul.com/api/data/v2/market-summary/?type=stock'
        data = requests.get(base_url).json()
        for stock_data in data:
            
            try:
                Stock.objects.update_or_create(
                    symbol=stock_data["symbol"],
                    defaults={
                        "ltp": (stock_data["close"]),
                        "point_change": (stock_data["point_change"]),
                        "percentage_change": (
                            stock_data["percentage_change"]
                        ),
                        "open_price": (stock_data["open"]),
                        "high_price": (stock_data["high"]),
                        "low_price": (stock_data["low"]),
                        "volume": (stock_data["volume"]),
                        "prev_close": (stock_data["prev_close"]),
                    },
                )
            except ValidationError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error processing stock {stock_data['symbol']}: {str(e)}"
                    )
                )


    def handle(self, *args, **options):
        self.sharesansar_scraper()

    