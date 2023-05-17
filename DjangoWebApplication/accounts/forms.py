from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AccountRegisterForm(forms.ModelForm):
    TYPES = (
        ('user', 'User'),
        ('organizer', 'Organizer'),
    )
    user_type = forms.ChoiceField(choices=TYPES)

    class Meta:
        model = Account
        fields = ['user_type', 'full_name', 'phone_number', 'date_of_birth', 'profile_pic', 'address', 'bio']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['full_name', 'date_of_birth', 'phone_number', 'address', 'bio']
