from celery import shared_task
from django.core.management import call_command

@shared_task
def sync_stock_data():
    call_command('sync_stock_data')
