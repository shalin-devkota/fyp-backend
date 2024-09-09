from bs4 import BeautifulSoup as soup
import requests
from stock.models import Stock
from django.core.management.base import BaseCommand
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "fix the description images"

    def safe_decimal(self,value):
        try:
            return Decimal(value.replace(",", ""))
        except InvalidOperation:
            return None

    # Function to safely convert to int
    def safe_int(self,value):
        try:
            return int(float(value.replace(",", "")))
        except ValueError:
            return None


    def get_stock_data(self):
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
                        },
                    )
                    stocks.append(stock_data)
                except ValidationError as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error processing stock {stock_data['symbol']}: {str(e)}"
                        )
                    )

    def merolagani_scraper(self): #Weird JS render going on here. Maybe i will do later maybe not dont know
        stocks = []
        base_url = "https://merolagani.com/LatestMarket.aspx"

        data_html = requests.get(base_url)
        data_soup = soup(data_html.text, "html.parser")
        table = data_soup.find(
            "div", {"id": "ctl00_ContentPlaceHolder1_LiveTrading"}
        ).find("table")
        field_names = [
            "symbol",
            "ltp",
            "percentage_change",
            "open",
            "high",
            "low",
            "volume",
            "prev_close",
            "point_change",
        ]

        for row in table.find_all("tr")[1:]:  # Skip the header row
            cells = row.find_all("td")
            print(cells)
            break
        
            stock_data = {
                field: cells[i].text.strip() for i, field in enumerate(field_names)
            }
            print(stock_data)
            break
            # Function to safely convert to Decimal
            # def safe_decimal(value):
            #     try:
            #         return Decimal(value.replace(',', ''))
            #     except InvalidOperation:
            #         return None

            # # Function to safely convert to int
            # def safe_int(value):
            #     try:
            #         return int(float(value.replace(',', '')))
            #     except ValueError:
            #         return None

            # try:
            #     Stock.objects.update_or_create(
            #         symbol=stock_data['symbol'],
            #         defaults={
            #             'ltp': safe_decimal(stock_data['ltp']),
            #             'point_change': safe_decimal(stock_data['point_change']),
            #             'percentage_change': safe_decimal(stock_data['percentage_change']),
            #             'open_price': safe_decimal(stock_data['open']),
            #             'high_price': safe_decimal(stock_data['high']),
            #             'low_price': safe_decimal(stock_data['low']),
            #             'volume': safe_int(stock_data['volume']),
            #             'prev_close': safe_decimal(stock_data['prev_close'])
            #         }
            #     )
            #     stocks.append(stock_data)
            # except ValidationError as e:
            #     self.stdout.write(self.style.ERROR(f"Error processing stock {stock_data['symbol']}: {str(e)}"))


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
        self.chukul_scraper()