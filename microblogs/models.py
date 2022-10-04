from django.db import models
# We import an abstract user class that we will be able to override to have our own model (see Django doc)
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    bio = models.TextField()
     
