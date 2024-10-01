# yourapp/management/commands/import_stocks.py

import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from stock.models import Stock
from decimal import Decimal
from datetime import datetime

class Command(BaseCommand):
    help = 'Import stock data from CSV file using bulk operations, keeping only the first occurrence of each unique (symbol, date) combination'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        batch_size = 10000  

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            
            count = 0
            processed = 0
            stocks_data = {}

            for row in reader:
                count += 1
                if row['Sector'] != 'N/A':
                    key = (row['Symbol'], row['Date'])
                    if key not in stocks_data:
                        stocks_data[key] = {
                            'symbol': row['Symbol'],
                            'ltp': Decimal(row['Close']),
                            'open_price': Decimal(row['Open']),
                            'high_price': Decimal(row['High']),
                            'low_price': Decimal(row['Low']),
                            'volume': int(row['Vol']),
                            'prev_close': Decimal(row['Close']),
                            'sector': row['Sector'].upper(),
                            'date': datetime.strptime(row['Date'], '%Y-%m-%d').date(),
                        }
                        processed += 1

                if len(stocks_data) >= batch_size:
                    self.process_batch(stocks_data)
                    stocks_data.clear()
                    self.stdout.write(f'Processed {processed} unique entries out of {count} total.')

            if stocks_data:
                self.process_batch(stocks_data)

            self.stdout.write(self.style.SUCCESS(f'Import completed. Processed {processed} unique entries out of {count} total.'))

    @transaction.atomic
    def process_batch(self, stocks_data):
        existing_stocks = Stock.objects.filter(
            symbol__in=[data['symbol'] for data in stocks_data.values()],
            date__in=[data['date'] for data in stocks_data.values()]
        ).values('id', 'symbol', 'date')

        existing_stocks_dict = {(stock['symbol'], stock['date']): stock['id'] for stock in existing_stocks}
        
        stocks_to_create = []
        stocks_to_update = []

        for key, data in stocks_data.items():
            if key in existing_stocks_dict:
                stock = Stock(id=existing_stocks_dict[key], **data)
                stocks_to_update.append(stock)
            else:
                stocks_to_create.append(Stock(**data))

        for stock in stocks_to_update + stocks_to_create:
            try:
                stock.point_change = stock.ltp - stock.prev_close
                stock.percentage_change = (stock.point_change / stock.prev_close) * 100
            except Exception as e:
                stock.point_change = 0.00
                stock.percentage_change = 0.00


        Stock.objects.bulk_create(stocks_to_create)


        if stocks_to_update:
            Stock.objects.bulk_update(stocks_to_update, [
                'ltp', 'open_price', 'high_price', 'low_price', 'volume',
                'prev_close', 'sector', 'point_change', 'percentage_change'
            ])