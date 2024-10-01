from rest_framework import serializers
from .models import CustomUser
from trading.models import Transaction
class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["fullname", "email", "username"]
    
class UserTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        