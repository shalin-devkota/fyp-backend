from rest_framework import serializers
from .models import Portfolio,PortfolioStock

class PortfolioStockSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source="stock.symbol")
    class Meta:
        model = PortfolioStock
        fields = ['id','stock','quantity','buying_price','symbol','created_at']

class PortfolioSerializer(serializers.ModelSerializer):
    stocks = PortfolioStockSerializer(many=True)
    class Meta:
        model = Portfolio
        fields = "__all__"

