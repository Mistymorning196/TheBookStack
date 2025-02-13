from django.db import models
from django.urls import reverse

# Create your models here.
class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
    
class Book(models.Model):
    '''
    Class for the model Book
    ''' 

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    #placeholder for image file
