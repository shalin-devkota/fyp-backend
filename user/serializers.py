from rest_framework import serializers
from .models import CustomUser
class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["fullname", "email", "username"]