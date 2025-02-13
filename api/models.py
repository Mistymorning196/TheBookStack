from django.db import models
#from django.urls import reverse
from django.contrib.auth.models import AbstractUser, Group, Permission


    
class Book(models.Model):
    '''
    Class for the model Book
    ''' 
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    #placeholder for image file

class SiteUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(default='2000-01-01')
    password = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def as_dict(self):
        return {  
            'id': self.id,  
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'date_of_birth': self.date_of_birth,
            'password': self.password,
        }
