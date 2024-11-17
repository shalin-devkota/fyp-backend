from rest_framework import serializers
from .models import CustomUser
from trading.models import Transaction
from trading.serializers import UserTransactionSerializer
from stock.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["fullname", "email", "username"]
    
class UserTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
    
class UserDashboardSerializer(serializers.Serializer):
    funds = serializers.DecimalField(max_digits=10, decimal_places=2)
    portfolio_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    recent_transactions = UserTransactionSerializer(many=True)
    streak=  serializers.IntegerField()
    top_performers = StockSerializer(many=True)
    worst_performers = StockSerializer(many=True)
    