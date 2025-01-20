from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=[('male', 'Мужской'), ('female', 'Женский')], widget=forms.RadioSelect, required=True,)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'gender']

class LoginForm(AuthenticationForm):
    pass
