from django.forms import forms,fields,widgets

class LoginForm(forms.Form):
    username=fields.CharField(max_length=200)
    password=fields.CharField(widget=widgets.PasswordInput())

class RegistrationForm(forms.Form):
    first_name=fields.CharField(max_length=100,min_length=1)
    last_name=fields.CharField(max_length=100,min_length=1)
    username=fields.CharField(max_length=100,min_length=1)
    email=fields.EmailField(max_length=100)
    password=fields.CharField(widget=widgets.PasswordInput())
    password1=fields.CharField(widget=widgets.PasswordInput())