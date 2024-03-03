from django import forms
from django.core.validators import RegexValidator
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User


class KBKForm(forms.Form):
    Name = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter Username!", 'style': 'width: 300px;'}), required=True)
    Email = forms.EmailField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your Email!",
               'style': 'width: 300px;'}), required=True)  # Use EmailField for email addresses
    Phone_no = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Mob number in format: +(Contrycode)XXXXXXXXXX",
               'style': 'width: 300px;', }), validators=[
        RegexValidator(regex=r'^\+\d{10,15}$', message='Enter a valid mobile number.',
                       code='invalid_mobile_number')], )  # This will validate the no and get only the integer value .

    Url = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please type your website URL", 'style': 'width: 300px;'}),
                          required=True)
    Company = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your company Name", 'style': 'width: 300px;'}))
    django_recaptcha = ReCaptchaField(label=False, required=True)


class Signup(UserCreationForm):
    username = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter the Username", 'style': 'width: 80%;'}),
                               required=True)
    first_name = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please enter the first_name",
               'style': 'width: 80%;', }))  # This will validate the no and get only the integer value .
    last_name = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please enter the last_name", 'style': 'width: 80%;'}),
                                required=True)
    email = forms.EmailField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Please Enter your Email",
               'style': 'width: 80%;'}), required=True)  # Use EmailField for email addresses
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'class': "form-cont", 'placeholder': "Please enter the Password", 'style': 'width: 80%;'}),
                                required=True)
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'class': "form-cont", 'placeholder': "Please re-enter the Password", 'style': 'width: 80%;'}),
                                required=True)


    django_recaptcha = ReCaptchaField(label=False, required=True)

    # def clean_email(self):  ## This is for email duplication check
    #     value = self.cleaned_data['email']
    #     if User.objects.filter(email=value).exists():
    #         raise forms.ValidationError("This email ID is already registered, Please signup with another one!")
    #     return value

    class meta:
        model = User
        field = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(Signup, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    def pass_to_email(self):
        data=[self.cleaned_data['email'], self.cleaned_data['first_name']]
        return data


class Signin(forms.Form):
    username = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Username",
               'style': 'width: 80%;'}), required=True)
    password = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'class': "form-cont", 'placeholder': "Password", 'style': 'width: 80%;'}),
                               required=True)
    django_recaptcha = ReCaptchaField(label=False, required=True)
    class meta:
        model = User
        field = ('username','password')


class Forgetpassword(forms.Form):
    username = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': "form-cont", 'placeholder': "Username",
               'style': 'width: 80%;'}), required=True)
    django_recaptcha = ReCaptchaField(label=False, required=True)
    class meta:
        model = User
        field = ('username')

class Changepassword(forms.Form):
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'class': "form-cont", 'placeholder': "Please enter the Password", 'style': 'width: 80%;'}),
                                required=True)
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'class': "form-cont", 'placeholder': "Please re-enter the Password", 'style': 'width: 80%;'}),
                                required=True)
    django_recaptcha = ReCaptchaField(label=False, required=True)

    class meta:
        model = User
        field = ('password1','password2')




