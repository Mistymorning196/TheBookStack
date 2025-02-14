from django.db import models
#from django.urls import reverse
from django.contrib.auth.models import AbstractUser, Group, Permission



    
class Book(models.Model):
    '''
    Class for the model Book
    ''' 
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    isbn = models.CharField(max_length=100)
    #placeholder for image file for cover picture
    #also need to add genres possibly a relationship? needs to be choices and able to do multiple
    #need relationship here for reviews should contain rating and review

class SiteUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(default='2000-01-01')
    password = models.CharField(max_length=100)
    #relationships here for users books multiple liked? currently reading? want to read?

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
