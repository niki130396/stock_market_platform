from djongo import models

# Create your models here.


class SomeTable(models.Model):
    some_field = models.CharField(max_length=120)
