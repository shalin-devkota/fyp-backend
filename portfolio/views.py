from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import PortfolioSerializer
from .models import Portfolio


# Create your views here.
class PortfolioView(ListAPIView):
    serializer_class = PortfolioSerializer
    def get_queryset(self):
        user = self.request.user
        return Portfolio.objects.filter(user=user)