''' import doc '''
from django.db import models

class CarInfo(models.Model):
    ''' class desc'''
    car_id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    series = models.CharField(max_length=2000)
    releaseDate = models.CharField(max_length=2000)
    odo_meter = models.IntegerField()
    cash_price = models.IntegerField()
    pre_pay = models.IntegerField()
    each_ins_amount = models.IntegerField()
    ins_num = models.IntegerField()
    description = models.CharField(max_length=500)
