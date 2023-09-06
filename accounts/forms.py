from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "profile_picture", "email", "password1", "password2"]
        # fields = ["username", "email", "password1", "password2"]