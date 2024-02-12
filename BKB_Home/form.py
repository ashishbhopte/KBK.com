from django import forms
from django.core.validators import RegexValidator
from django_recaptcha.fields import ReCaptchaField



class KBKForm(forms.Form):
    Name = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your Name!", 'style': 'width: 300px;'}),required=True)
    Email = forms.EmailField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your Email!",
               'style': 'width: 300px;'}), required=True)  # Use EmailField for email addresses
    Phone_no = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please no in format: +(Contrycode)XXXXXXXXXX",
               'style': 'width: 300px;',}),validators=[RegexValidator(regex=r'^\+\d{10,15}$',message='Enter a valid mobile number.', code='invalid_mobile_number')],)  # This will validate the no and get only the integer value .

    Url = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please type your website URL", 'style': 'width: 300px;'}), required=True)
    Company = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your company Name", 'style': 'width: 300px;'}))
    django_recaptcha = ReCaptchaField(label=False,required=True)


class Signup(forms.Form):
    Name = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your Name!", 'style': 'width: 80%;'}),required=True)
    Email = forms.EmailField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your Email!",
               'style': 'width: 80%;'}), required=True)  # Use EmailField for email addresses
    Phone_no = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please no in format: +(Contrycode)XXXXXXXXXX",
               'style': 'width: 80%;',}),validators=[RegexValidator(regex=r'^\+\d{10,15}$',message='Enter a valid mobile number.', code='invalid_mobile_number')],)  # This will validate the no and get only the integer value .

    Url = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please type your website URL", 'style': 'width: 80%;'}), required=True)
    Company = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your company Name", 'style': 'width: 80%;'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'class': "form-cont",'placeholder': "Please enter the Password", 'style': 'width: 80%;'}), required=True)
    rpassword = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'class': "form-cont", 'placeholder': "Please re-enter the Password", 'style': 'width: 80%;'}), required=True)
    def clean(self):
        cleaned_data = super().clean()  # ye validation logic maintain ke liye hai
        pwdval = cleaned_data['password']
        rpwdval = cleaned_data['rpassword']
        if pwdval != rpwdval:
            raise forms.ValidationError('Password Not Matched !')

    django_recaptcha = ReCaptchaField(label=False,required=True)
