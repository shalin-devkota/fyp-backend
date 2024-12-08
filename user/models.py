from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from stock.models import Stock
from datetime import datetime
class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    available_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
   
    def __str__(self):
        return self.username

    def get_portfolio_value(self):
        portfolio = self.user_portfolio.first()
        total_value = 0 
        for stock in portfolio.stocks.all():
            stock_obj = Stock.objects.get(symbol=stock.stock.symbol,date=datetime.today())
            total_value += stock_obj.ltp * stock.quantity
        return total_value
    
    def get_recent_trades(self):
        return self.user_transactions.all().order_by("-created_at")[:5]
    
    def get_trading_streak(self):
        transactions = self.user_transactions.all().order_by("created_at")

        if not transactions:
            return 0
        
        streak = 0
        last_transaction = transactions[0]
        for transaction in transactions[1:]:
       
            date_diff=  (transaction.date - last_transaction.date).days

         
            if date_diff == 1:
                streak += 1

            elif date_diff == 0:
                return 1
            else:
                return streak
            
            last_transaction = transaction
    
    
        
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

