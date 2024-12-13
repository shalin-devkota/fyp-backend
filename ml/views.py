from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
# Create your views here.

class PredictView(APIView):
    def get(self,request,*args,**kwargs):
        symbol = request.query_params.get('symbol')
        request_url = f"http://localhost:5000/?symbol={symbol}"
        response = requests.get(request_url)
        return Response(response.json())
    
