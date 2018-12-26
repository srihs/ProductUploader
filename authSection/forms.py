from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)

User =get_user_model()

class userLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username','required':'true','autofocus':'true'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password','required':'true','autofocus':'true'}))

    def clean(self,*args, **kwargs):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(
                    'Oh! I can\'t find that user - create user first!')
            elif not user.check_password(password):
                raise forms.ValidationError(
                    'Oh! That password is incorrect - try again!')
            elif not user.is_active:
                raise forms.ValidationError(
                    'Oh! That user is not active in the database!')
