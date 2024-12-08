from django.shortcuts import render
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserLoginSerializer, UserTransactionSerializer, UserDashboardSerializer
from rest_framework.generics import ListAPIView
from trading.models import Transaction
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
    