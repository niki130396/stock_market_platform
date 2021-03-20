from djongo import models

# Create your models here.


class StatementsMetaData(models.Model):
    company_id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    market_cap = models.BigIntegerField(blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    ipo_year = models.IntegerField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
