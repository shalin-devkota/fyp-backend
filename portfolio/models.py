from stock.models import PortfolioStock, DateTimeModel
from user.models import CustomUser
from django.db import models


class Portfolio(DateTimeModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="user_portfolio")
    stocks = models.ManyToManyField(PortfolioStock,related_name="portfolio_stocks")

    def __str__(self):
        return f"{self.user.username}'s Portfolio"