from django.shortcuts import render,get_list_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import StockSerializer
from .models import Stock

from rest_framework.exceptions import ParseError
from rest_framework.views import APIView

from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from  rest_framework import status
from django.utils import timezone
class ListStock(ListAPIView):
    serializer_class = StockSerializer
    pagination_class = None
    
    def get_queryset(self):
        today = timezone.now().date()
        sector = self.request.query_params.get("sector")
        if sector:
            return Stock.objects.filter(sector__iexact=sector,date=today)
        return Stock.objects.filter(date=today)
    
class StockDetail(APIView):
    serializer_class = StockSerializer
    
    def get(self, request, *args, **kwargs):

        year = request.GET.get("year")
        month = request.GET.get("month")
        portfolio = request.user.user_portfolio.first()

        symbol = kwargs.get("symbol")
        
        stock_history = dict()
        if not year or not month:
            raise ParseError("Both 'year' and 'month' must be provided.")

       
        queryset = Stock.objects.filter(symbol__iexact=symbol, date__year=year, date__month=month)

        stocks = get_list_or_404(queryset)
        

        serializer = self.serializer_class(stocks, many=True)
        for x in serializer.data:
            stock_history[x["date"]] = {"open": x["open_price"], "close": x["ltp"], "low": x["low_price"], "high": x["high_price"]}
        data = {
            "symbol": symbol,
            "number_of_stocks": sum([x.quantity for x in portfolio.stocks.filter(stock__symbol__iexact=symbol).all()]),
            "history" : stock_history
        }
        return Response(data,status=status.HTTP_200_OK)