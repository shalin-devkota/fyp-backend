from django.shortcuts import render
from .models import CustomUser,UserWishlistItem
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserLoginSerializer, UserTransactionSerializer, UserDashboardSerializer
from rest_framework.generics import ListAPIView
from trading.models import Transaction
from stock.models import Stock
from stock.serializers import StockSerializer
# Create your views here.

class GetUserFromJWT(APIView):
    def get(self,request,*args,**kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        print(token)
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token_obj = AccessToken(token.split(" ")[1])

        user_queryset = CustomUser.objects.filter(id=token_obj["user_id"])
        if not user_queryset.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = user_queryset.values("username", "email").first()
        serializer = UserLoginSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserTransactions(ListAPIView):
    serializer_class = UserTransactionSerializer
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)
    
class LoadFunds(APIView):
    def post(self,request,*args,**kwargs):
        amount = request.data.get("amount")
        if not amount:
            return Response({"error": "Amount is required."}, status=400)
        try:
            user = request.user
            user.available_funds += int(amount)
            user.save()
            return Response({"message": "Funds loaded successfully."}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class GetFunds(APIView):
    def get(self,request,*args,**kwargs):
        user = request.user
        return Response({"funds": user.available_funds}, status=200)

class DashboardView(APIView):
    def get(self,request,*args,**kwargs):
        user = request.user
        total_portfolio_value = user.get_portfolio_value()
        portfolio = user.user_portfolio.first()
        top_performers = portfolio.get_top_performers()
        worst_performers = portfolio.get_worst_performers()
        profit_or_loss=portfolio.get_profit_or_loss()
        recent_trades = user.get_recent_trades()
        streak = user.get_trading_streak()
     
        response = UserDashboardSerializer({
            "funds": user.available_funds,
            "portfolio_value": total_portfolio_value,
            "top_performers": top_performers,
            "worst_performers": worst_performers,
            "recent_transactions": recent_trades,
            "streak": streak,
            "profit_or_loss": profit_or_loss
        })
        return Response(response.data, status=200)
    
class WishlistStock(APIView):
    def post(self,request,*args,**kwargs):
        user = request.user
        symbol = request.data.get("symbol")
        if not symbol:
            return Response({"error": "Stock symbol is required."}, status=400)
        stock = Stock.objects.filter(symbol=symbol).first()
        if not stock:
            return Response({"error": "Stock not found."}, status=400)
        wishlist_obj, created = UserWishlistItem.objects.get_or_create(user=user, stock=stock)
        if not created:
            return Response({"error": "Stock already in wishlist."}, status=400)
        return Response({"message": "Stock added to wishlist."}, status=201)


class GetWishList(APIView):
    def get(self,request,*args,**kwargs):
        wishlist_items = UserWishlistItem.objects.filter(user=request.user)
        stocks = [item.stock for item in wishlist_items]
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)


class RemoveFromWishlistView(APIView):
    def delete(self, request, symbol):
        try:
            stock = Stock.objects.filter(symbol__iexact=symbol).first()
            wishlist_item = UserWishlistItem.objects.get(
                user=request.user, 
                stock= stock
            )
            wishlist_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserWishlistItem.DoesNotExist:
            return Response(
                {"detail": "Stock not found in wishlist"}, 
                status=status.HTTP_404_NOT_FOUND
            )