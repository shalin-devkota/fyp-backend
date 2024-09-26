from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import StockSerializer
from .models import Stock

class ListAllStock(ListAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.filter(deleted_at=None)
