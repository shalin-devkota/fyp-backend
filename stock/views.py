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
from datetime import datetime
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
            stock_history[x["date"]] = {"open": x["open_price"], "close": x["ltp"], "low": x["low_price"], "high": x["high_price"],"volume":x['volume']}
        data = {
            "symbol": symbol,
            "number_of_stocks": sum([x.quantity for x in portfolio.stocks.filter(stock__symbol__iexact=symbol).all()]),
            "history" : stock_history
        }
        return Response(data,status=status.HTTP_200_OK)
    
class StockRange(APIView):
    serializer_class = StockSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            # Get date parameters from query params
            from_date = request.query_params.get('from')
            to_date = request.query_params.get('to')
            
            # Validate date parameters
            if not from_date or not to_date:
                return Response(
                    {"error": "Both 'from' and 'to' dates are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Convert string dates to datetime objects
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Validate date range
            if from_date > to_date:
                return Response(
                    {"error": "From date must be before or equal to to date"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get user portfolio
            portfolio = request.user.user_portfolio.first()
            if not portfolio:
                return Response(
                    {"error": "User portfolio not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get symbol from URL parameters
            symbol = kwargs.get("symbol")
            if not symbol:
                return Response(
                    {"error": "Symbol is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Initialize stock history dictionary
            stock_history = dict()
            
            # Query stocks within date range
            queryset = Stock.objects.filter(
                symbol__iexact=symbol,
                date__range=[from_date, to_date]
            ).order_by('date')
            
            # Get stocks or return 404
            stocks = get_list_or_404(queryset)
            
            # Serialize the data
            serializer = self.serializer_class(stocks, many=True)
            
            # Build stock history dictionary
            for stock_data in serializer.data:
                stock_history[stock_data["date"]] = {
                    "open": stock_data["open_price"],
                    "close": stock_data["ltp"],
                    "low": stock_data["low_price"],
                    "high": stock_data["high_price"],
                    "volume": stock_data["volume"]
                }
            
            # Calculate total quantity of stocks owned
            total_quantity = sum(
                x.quantity 
                for x in portfolio.stocks.filter(stock__symbol__iexact=symbol).all()
            )
            
            # Prepare response data
            data = {
                "symbol": symbol,
                "number_of_stocks": total_quantity,
                "history": stock_history
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
