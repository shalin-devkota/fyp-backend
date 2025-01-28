from django.core.management.base import BaseCommand
from django.db import transaction
from stock.models import Stock
from decimal import Decimal
from datetime import datetime
import csv

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
                    try:
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
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Error processing row {count}: {str(e)}'))
                        continue

            if stocks_data:
                self.process_batch(stocks_data)

            self.stdout.write(self.style.SUCCESS(f'Import completed. Processed {processed} unique entries out of {count} total.'))

    @transaction.atomic
    def process_batch(self, stocks_data):
        # First, get all existing stocks for the batch
        existing_stocks = set(
            Stock.objects.filter(
                symbol__in=[data['symbol'] for data in stocks_data.values()],
                date__in=[data['date'] for data in stocks_data.values()]
            ).values_list('symbol', 'date')
        )

        # Separate data into create and skip lists
        stocks_to_create = []
        for (symbol, date), data in stocks_data.items():
            # Calculate point_change and percentage_change
            try:
                point_change = data['ltp'] - data['prev_close']
                percentage_change = (point_change / data['prev_close']) * 100
            except Exception:
                point_change = Decimal('0.00')
                percentage_change = Decimal('0.00')

            # Only create if it doesn't exist
            if (symbol, date) not in existing_stocks:
                stock = Stock(
                    point_change=point_change,
                    percentage_change=percentage_change,
                    **data
                )
                stocks_to_create.append(stock)

        # Bulk create only new records
        if stocks_to_create:
            try:
                Stock.objects.bulk_create(stocks_to_create, ignore_conflicts=True)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error during bulk create: {str(e)}'))