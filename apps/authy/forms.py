from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    PasswordResetForm,
)
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for creating new users, using the custom User model.
    """

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    """
    Custom form for changing user information, using the custom User model.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")


class CustomUserLoginForm(forms.Form):
    """
    Custom user login form used to validate login credentials.
    """

    email = forms.CharField(label="Email Address", widget=forms.EmailInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")


class CustomPasswordResetForm(PasswordResetForm):
    """
    Custom form for resetting user passwords, using the custom User model.
    """

    class Meta:
        model = User
        fields = "__all__"
