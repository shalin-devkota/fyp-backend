from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import StockSerializer
from .models import Stock
from django.shortcuts import get_object_or_404

class ListStock(ListAPIView):
    serializer_class = StockSerializer
    
    def get_queryset(self):
        sector = self.request.query_params.get("sector")
        if sector:
            return Stock.objects.filter(sector__iexact=sector)
        return Stock.objects.all()
    
class StockDetail(RetrieveAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    lookup_field = "symbol"
    lookup_url_kwarg = "symbol"

    def get_object(self):
        symbol = self.kwargs.get(self.lookup_url_kwarg)
    
        return get_object_or_404(Stock, symbol__iexact=symbol)