from stock.models import PortfolioStock, DateTimeModel, Stock
from user.models import CustomUser
from django.db import models
from stock.serializers import StockSerializer
from datetime import datetime

class Portfolio(DateTimeModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="user_portfolio")
    stocks = models.ManyToManyField(PortfolioStock,related_name="portfolio_stocks")

    def __str__(self):
        return f"{self.user.username}'s Portfolio"
    
    def get_top_performers(self):
        top_performer = self.stocks.all().order_by("stock__percentage_change")[:5]
        stocks = Stock.objects.filter(id__in=[stock.stock.id for stock in top_performer])
        return stocks
    
    def get_worst_performers(self):
        worst_performer = self.stocks.all().order_by("-stock__percentage_change")[:5]
        stocks = Stock.objects.filter(id__in=[stock.stock.id for stock in worst_performer])
        return stocks

    def get_profit_or_loss(self):
        stocks = self.stocks.all()
        stock_prices = 0
        for stock in stocks:
            if stock.quantity > 0:
                stock_prices += stock.buying_price * stock.quantity
        current_portfolio_value = self.user.get_portfolio_value()
        return current_portfolio_value - stock_prices