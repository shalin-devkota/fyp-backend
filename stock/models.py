from django.db import models

# Create your models here.

SECTOR_CHOICES = (
    ("CAPITAL","Capital"),
    ("COMMERICAL BANKS", "Commerical Banks"),
    ("CORPORATE DEBENTURE", "Corporate Debenture"),
    ("DEVELOPMENT BANK LIMITED", "Development Bank Limited"),
    ("FINANCE", "Finance"),
    ("GOVERNMENT BOND", "Government Bond"),
    ("HOTELS AND TOURISM", "Hotels and Tourism"),
    ("HYDRO POWER", "Hydro Power"),
    ("INVESTMENT", "Investment"),
    ("LIFE INSURANCE", "Life Insurance"),
    ("MANUFACTURING AND PROCESSING", "Manufacturing and Processing"),
    ("MICROFINANCE", "Microfinance"),
    ("MUTUAL FUND", "Mutual Fund"),
    ("NON LIFE INSURANCE","Non life Insurance"),
    ("OTHERS", "Others"),
    ("PREFERRED STOCK", "Preferred Stock"),
    ("PROMOTER SHARE", "Promoter Share"),
    ("TRADINGS","Tradings"),

)
class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class Stock(DateTimeModel):
    symbol = models.CharField(max_length=10,db_index=True)
    ltp = models.DecimalField(max_digits=10, decimal_places=2)
    point_change = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_change = models.DecimalField(max_digits=10, decimal_places=2)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    prev_close = models.DecimalField(max_digits=10, decimal_places=2)
    sector = models.CharField(max_length=200,choices=SECTOR_CHOICES,null=True,blank=True)
    date = models.DateField(null=True,blank=True) 


    def __str__(self):
        return self.symbol

    class Meta:
        unique_together = ['symbol','date']

class PortfolioStock(DateTimeModel):
    symbol = models.ForeignKey(Stock,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.symbol} - {self.quantity}"
    
  