from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
         model = CustomUser
         fields = UserCreationForm.Meta.fields + ('gender',)

class LoginForm(AuthenticationForm):
    pass
