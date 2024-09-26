from django.shortcuts import render
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserLoginSerializer

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
        user = user_queryset.values("fullname", "email").first()
        serializer = UserLoginSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
