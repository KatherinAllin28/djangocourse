from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from .storages import ImageLocalStorage


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    #price = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    created_at = models.DateTimeField(auto_now_add=True)
    #description = models.TextField(blank=True, null=True)
    #created_at = models.DateTimeField(null=True, blank=True)
    #updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class Comment(models.Model):
      product = models.ForeignKey(Product, on_delete=models.CASCADE)
      description = models.TextField()

class Cart(models.Model):
    pass

class MyModel(models.Model):
    image = models.ImageField(storage=ImageLocalStorage(), upload_to='uploads/')
