from rest_framework import serializers

from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        exclude = ["created_at","updated_at","deleted_at"]



    