from django.db import models
from django.core.validators import RegexValidator  # for regular expression in django


# Create your models here.
class KBKform(models.Model):
    Name = models.CharField(max_length=70, null=False, blank=False)
    Email = models.EmailField(unique=True)  # Use EmailField for email addresses
    Phone_no = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{10,15}$','Enter a valid mobile number.')])  # This will validate the no and get only the integer value .
    Url = models.TextField()
    Company = models.CharField(max_length=100, null=False, blank=False)
    Date = models.DateField()

    def __str__(self):
        return self.Name
    print('this is module.py ')
