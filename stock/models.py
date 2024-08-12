from django.db import models

# Create your models here.
class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Stock(DateTimeModel):
    symbol = models.CharField(max_length=10,unique=True)
    ltp = models.DecimalField(max_digits=10, decimal_places=2)
    point_change = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_change = models.DecimalField(max_digits=10, decimal_places=2)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    prev_close = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.symbol