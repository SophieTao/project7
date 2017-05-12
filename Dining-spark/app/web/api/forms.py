from django import forms
from django.contrib.admin import widgets

class LoginForm(forms.Form):
	username = forms.CharField(label='Username',max_length=32)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class CreateListingForm(forms.Form):
	name = forms.CharField(label='Name',max_length=32)
	location = forms.CharField(label='Location', max_length=32)
	description = forms.CharField(label='Description', max_length=300)	
	date = forms.DateTimeField(label='Date')
	Calories = forms.IntegerField(label='Calories')

class CreateAccountForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Query', max_length=200)