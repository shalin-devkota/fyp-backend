from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from stock.models import Stock
from datetime import datetime
from decimal import Decimal
import numpy as np
# Create your views here.

class PredictView(APIView):
    def get(self,request,*args,**kwargs):
        symbol = request.query_params.get('symbol')
        request_url = f"http://localhost:5000/?symbol={symbol}"
        response = requests.get(request_url)
        
        response = response.json()
        _ = response.pop(datetime.today().strftime('%Y-%m-%d'))
        print(response)
        prices = [y for y in response.values()]
        max_price = max(prices)
        min_price = min(prices)
        current_price = Stock.objects.get(symbol=symbol,date= datetime.today()).ltp
        current_price = Decimal(current_price)
        potential_gain = Decimal(max_price) - current_price
        potential_loss = current_price - Decimal(min_price)
        

        mean_price = sum(prices)/len(prices)
        squared_diffs = [(price-mean_price)**2 for price in prices]
        variance = sum(squared_diffs)/len(prices)

        volatility = variance ** 0.5

        threshold = float(current_price) * 0.01
        threshold = Decimal(threshold)
        buy_count , sell_count , hold_count = 0,0,0

        risk_reward_ratio = current_price * Decimal(volatility) / 100

        for price in prices:
            if price> current_price + threshold:
                buy_count += 1
            elif price < current_price - threshold:
                sell_count += 1
            else:
                hold_count += 1

        buy_prob = buy_count/len(prices) *100
        sell_prob = sell_count/len(prices) * 100
        hold_prob = hold_count/len(prices) * 100
        


        data = {
            "predictions": response,
            "potential_gain": max(0,potential_gain),
            "potential_loss": max(0,potential_loss),
            "risk_reward_ratio": risk_reward_ratio,
            "volatility": volatility,
            "buy_probability": buy_prob,
            "sell_probability": sell_prob,
            "hold_probability": hold_prob

        }
        return Response(data)
    
