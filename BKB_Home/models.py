from django.db import models
from django.core.validators import RegexValidator  # for regular expression in django
from django.contrib.auth.models import User


# Create your models here.
class KBKform(models.Model):
    Name = models.CharField(max_length=70, null=False, blank=False, unique=True)
    Email = models.EmailField(unique=True)  # Use EmailField for email addresses
    Phone_no = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{10,15}$',
                                                                          'Enter a valid mobile number.')])  # This will validate the no and get only the integer value .
    Url = models.CharField(max_length=255, unique=True)
    Company = models.CharField(max_length=100, null=False, blank=False)
    Date = models.DateField()

    def __str__(self):
        return self.Name


class signup_model(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_tocken = models.CharField(max_length=100, default=None)
    is_verified = models.BooleanField(default=False)  # This field have to reflect in my admin user model also usko vies.py se hadle karna bad me
    # image = models.ImageField(upload_to='static/userimage/',null=True,unique=False)
    # feedback = models.TextField(max_length=500,blank=True, null=True)
    def __str__(self):
        return self.user.username
