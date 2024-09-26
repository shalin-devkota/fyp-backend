from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import StockSerializer
from .models import Stock

class ListStock(ListAPIView):
    serializer_class = StockSerializer
    
    def get_queryset(self):
        sector = self.request.query_params.get("sector")
        if sector:
            return Stock.objects.filter(sector__iexact=sector)
        return Stock.objects.all()
    
