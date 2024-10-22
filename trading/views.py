from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction
from django.utils import timezone
from stock.models import Stock
from portfolio.models import Portfolio, PortfolioStock

# Create your views here.
class BuyStock(APIView):
    def post(self, request, *args, **kwargs):
        symbol = request.data.get("symbol")
        quantity = request.data.get("quantity")
        today = timezone.now().date()
        stock = Stock.objects.filter(symbol__iexact=symbol, date=today).first()
        unit_price = stock.ltp

        quantity = int(quantity)
        if not symbol or not quantity or not unit_price:
            return Response({"error": "symbol, quantity and unit_price are required."}, status=400)
        try:
            user_portfolio,created = Portfolio.objects.get_or_create(user=request.user)
            stock = PortfolioStock.objects.create(stock=stock,quantity=quantity,buying_price=unit_price)
            available_funds = request.user.available_funds
            if available_funds < unit_price:
                return Response({"error": "Insufficient funds."}, status=400)
            request.user.available_funds -= unit_price * quantity
            request.user.save()
            user_portfolio.stocks.add(stock)
            Transaction.objects.create(user=request.user, symbol=symbol, quantity=quantity, unit_price=unit_price,action="BUY")

            return Response({"message": "Transaction successful."}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

class SellStock(APIView):
    def post(self, request, *args, **kwargs):
        portfolio_stock_id  = request.data.get("id")
        quantity = int(request.data.get("quantity",0))
        today = timezone.now().date()
        portfolio_stock = PortfolioStock.objects.filter(id=portfolio_stock_id).first()
        ltp = Stock.objects.filter(symbol = portfolio_stock.stock.symbol, date=today).first().ltp

        
        if not portfolio_stock:
            return Response({"error": "Stock does not exist in your portfolio."}, status=400)
        
        if quantity > portfolio_stock.quantity:
            return Response({"error": "You do not have enough units to sell."}, status=400)
        
        if quantity == 0:
            return Response({"error": "Specify a valid quantity to sell."}, status=400)
        
        portfolio_stock.quantity -= quantity
        portfolio_stock.save()
        request.user.available_funds += ltp * quantity
        request.user.save()
        Transaction.objects.create(user=request.user, symbol=portfolio_stock.stock.symbol, quantity=quantity, unit_price=ltp,action="SELL")
        return Response({"message": "Transaction successful."}, status=201)
        

