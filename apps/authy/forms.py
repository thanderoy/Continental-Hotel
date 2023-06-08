from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import authenticate

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for creating new users, using the custom User model.
    """

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email",
            "password1", "password2"
        )


class CustomUserChangeForm(UserChangeForm):
    """
    Custom form for changing user information, using the custom User model.
    """

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "password"
        )


class CustomUserLoginForm(forms.Form):
    """
    Custom user login form used to validate login credentials.
    """

    email = forms.CharField(
        label="Email Address", widget=forms.EmailInput
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self) -> None:
        """
        Checks if the provided email and password are valid and raises a
            validation error if they are not.
        """
        if self.is_valid():
            form = self.cleaned_data

            email = form.get("email")
            password = form.get("password")

            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Credentials")
