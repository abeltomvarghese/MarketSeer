# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class WeeklyTimeseriesUnadjusted(models.Model):
    weekly_symbol = models.CharField(max_length=10)
    stock_open = models.DecimalField(max_digits=10, decimal_places=4)
    stock_high = models.DecimalField(max_digits=10, decimal_places=4)
    stock_low = models.DecimalField(max_digits=10, decimal_places=4)
    stock_close = models.DecimalField(max_digits=10, decimal_places=4)
    stock_adj_close = models.DecimalField(max_digits=10, decimal_places=4)
    stock_volume = models.BigIntegerField()
    dividend_amount = models.DecimalField(max_digits=10, decimal_places=4)
    cobdate_partition = models.DateField()

    class Meta:
        managed = False
        db_table = 'weekly_timeseries_unadjusted'


class Stock(models.Model):
    symbol = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'stock'
