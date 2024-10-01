from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction
from django.utils import timezone
from stock.models import Stock
# Create your views here.
class BuyStock(APIView):
    def post(self, request, *args, **kwargs):
        symbol = request.data.get("symbol")
        quantity = request.data.get("quantity")
        today = timezone.now().date()
        stock = Stock.objects.filter(symbol__iexact=symbol, date=today).first()
        unit_price = stock.ltp


        if not symbol or not quantity or not unit_price:
            return Response({"error": "symbol, quantity and unit_price are required."}, status=400)
        try:
            transaction = Transaction.objects.create(user=request.user, symbol=symbol, quantity=quantity, unit_price=unit_price,action="BUY")
            return Response({"message": "Transaction successful."}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

class SellStock(APIView):
    def post(self, request, *args, **kwargs):
        symbol = request.data.get("symbol")
        quantity = int(request.data.get("quantity"))
        today = timezone.now().date()
        stock = Stock.objects.filter(symbol__iexact=symbol, date=today).first()
        unit_price = stock.ltp
        total_units = 0


        if not symbol or not quantity or not unit_price:
            return Response({"error": "symbol, quantity and unit_price are required."}, status=400)
        
        transactions = Transaction.objects.filter(user=request.user, symbol=symbol)
        for x in transactions:
            total_units += x.quantity
        
        if quantity > total_units:
            return Response({"error": "You do not have enough units to sell."}, status=400)
    
        try:
            transaction = Transaction.objects.create(user=request.user, symbol=symbol, quantity=quantity, unit_price=unit_price,action="SELL")
            return Response({"message": "Transaction successful."}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

