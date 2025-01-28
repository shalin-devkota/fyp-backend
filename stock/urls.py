from django.urls import path
from .views import *
urlpatterns = [
    path("list/", ListStock.as_view(), name="list_all_stock"),
    path("detail/<str:symbol>/", StockDetail.as_view(), name="stock_detail"),
    path("range/<str:symbol>/", StockRange.as_view(), name="stock_detail"),
]


