from rest_framework.serializers import ModelSerializer
from .models import Transaction

class UserTransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"