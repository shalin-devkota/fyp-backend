from bs4 import BeautifulSoup as soup
import requests
from stock.models import Stock
from django.core.management.base import BaseCommand
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = "fix the description images"

    def handle(self, *args, **options):
        self.get_stock_data()
       

    def get_stock_data(self):
        stocks = []
        base_url = 'https://www.sharesansar.com/live-trading'
        
        data_html = requests.get(base_url)
        data_soup = soup(data_html.text, 'html.parser')
        
        table = data_soup.find('table', {'id': 'headFixed'})
        
        # Define the order of the fields
        field_names = [
            'id', 'symbol', 'ltp', 'point_change', 
            'percentage_change', 'open', 'high', 'low', 
            'volume', 'prev_close'
        ]
        
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cells = row.find_all('td')
            if len(cells) == len(field_names):  # Ensure there are enough cells
                stock_data = {field: cells[i].text.strip() for i, field in enumerate(field_names)}
                
                # Function to safely convert to Decimal
                def safe_decimal(value):
                    try:
                        return Decimal(value.replace(',', ''))
                    except InvalidOperation:
                        return None

                # Function to safely convert to int
                def safe_int(value):
                    try:
                        return int(float(value.replace(',', '')))
                    except ValueError:
                        return None

                try:
                    Stock.objects.update_or_create(
                        symbol=stock_data['symbol'],
                        defaults={
                            'ltp': safe_decimal(stock_data['ltp']),
                            'point_change': safe_decimal(stock_data['point_change']),
                            'percentage_change': safe_decimal(stock_data['percentage_change']),
                            'open_price': safe_decimal(stock_data['open']),
                            'high_price': safe_decimal(stock_data['high']),
                            'low_price': safe_decimal(stock_data['low']),
                            'volume': safe_int(stock_data['volume']),
                            'prev_close': safe_decimal(stock_data['prev_close'])
                        }
                    )
                    stocks.append(stock_data)
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f"Error processing stock {stock_data['symbol']}: {str(e)}"))
            
            

    
