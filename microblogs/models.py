from django.db import models
# We import an abstract user class that we will be able to override to have our own model (see Django doc)
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.

class User(AbstractUser):
    # We create custom validators, RegexValidator checks a value against a regular expression
    # for creating regex: ^ means beginning of the sentence, $ to the end, \w{min,max} means at leasth min and at most max alphaneumericals
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex = r'^@\w{3,}$',
            message = 'Username must consist of @ followed by at least three alphaneumericals'
        )]
    )

    first_name = models.CharField(max_length = 50, blank=False, unique = False)
    last_name = models.CharField(max_length = 50, blank=False, unique = False)
    email = models.EmailField(unique = True, blank = False)
    bio = models.CharField(blank = True, unique = False, max_length = 520)
