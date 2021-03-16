from djongo import models

# Create your models here.


class SomeTable(models.Model):
    """
    Test pre-commit
    """

    some_field = models.CharField(max_length=120)
