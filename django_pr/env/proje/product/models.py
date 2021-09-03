from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=250)
    price = models.CharField(max_length=250)
    sale = models.CharField(max_length=5)