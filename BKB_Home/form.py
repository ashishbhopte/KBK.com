from django import forms
from django.core.validators import RegexValidator
from django_recaptcha.fields import ReCaptchaField



class KBKForm(forms.Form):
    Name = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your name!", 'style': 'width: 300px;'}),required=True)
    Email = forms.EmailField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your Email!",
               'style': 'width: 300px;'}), required=True)  # Use EmailField for email addresses
    Phone_no = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please no in format: +(Contrycode)XXXXXXXXXX",
               'style': 'width: 300px;',}),validators=[RegexValidator(regex=r'^\+\d{10,15}$',message='Enter a valid mobile number.', code='invalid_mobile_number')],)  # This will validate the no and get only the integer value .

    Url = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please type your website url", 'style': 'width: 300px;'}), required=True)
    Company = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your company name", 'style': 'width: 300px;'}))
    django_recaptcha = ReCaptchaField(label=False,required=True)
