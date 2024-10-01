from django.db import models
from user.models import CustomUser
from stock.models import DateTimeModel, Stock
# Create your models here.


class Transaction(DateTimeModel):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_transactions")
    quantity = models.PositiveIntegerField(null=True,blank=True)
    symbol = models.CharField(max_length=10,null=True,blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    date = models.DateField(auto_now=True)
    action = models.CharField(max_length=10,choices=(("BUY","BUY"),("SELL","SELL")),null=True,blank=True)

    def __str__(self):
        return f"{self.user} - {self.symbol} {self.unit_price}"
