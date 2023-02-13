from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
# from django.forms.fields import DateField


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),)
    last_name = forms.CharField(max_length=101,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),help_text="Required")

    class Meta:
        model = User
        fields =['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter User Name'})
        }
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password','style':'display:inline-block;','id':'id_password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})

class BlogForm(forms.ModelForm):
    # date=DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    class Meta:
        model=Blogpost
        fields="__all__"
        widgets={
            'user':forms.TextInput(attrs={'id': 'auth_ip','value':"",'type':'hidden'})
        }