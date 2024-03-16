from django import forms
from django.forms import ClearableFileInput
from .models import Event


# Form to create accounts
class CreateAccountForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'in_input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'in_input'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'in_input'}))

# Form to create accounts
class SignForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'in_input'}))
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'class': 'in_input'}))

# Form to create accounts
class eventForm(forms.Form):
    name = forms.CharField(required=True)
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
    location = forms.CharField(required=True)
    image = forms.ImageField(required=True, widget=ClearableFileInput(attrs={'multiple': False}))

