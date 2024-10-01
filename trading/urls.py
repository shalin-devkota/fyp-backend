from django.urls import path
from .views import *
urlpatterns = [
    path("buy/", BuyStock.as_view(), name="buy-stock"),
    path("sell/", SellStock.as_view(), name="sell-stock"),
]

