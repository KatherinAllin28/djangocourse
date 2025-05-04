from django.db import models

# Create your models here.
class ToDo(models.Model):  
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    memo = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
