from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class PredictView(APIView):
    def get(self,request,*args,**kwargs):
        predict()