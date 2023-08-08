from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomPasswordResetForm
from .models import User


def register_user(request):
    if request.method == "GET":
        form = CustomUserCreationForm()

    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("authy:login")

        else:
            form = CustomUserCreationForm()

    context = {"form": form}

    return render(request, "authy/register.html", context)


def login_user(request):
    if request.method == "GET":
        form = CustomUserLoginForm()

    elif request.method == "POST":
        form = CustomUserLoginForm(request.POST)

        if form.is_valid():
            form = form.cleaned_data
            user = authenticate(
                username=form.get("email"), password=form.get("password")
            )

            if user is not None:
                login(request, user)
                return redirect("hotel:room_offering")
            else:
                form = CustomUserLoginForm()

    context = {"form": form}

    return render(request, "authy/login.html", context)


def logout_user(request):
    logout(request)
    return redirect("hotel:room_offering")


def password_reset(request):
    if request.method == "GET":
        form = CustomPasswordResetForm()

    elif request.method == "POST":
        form = CustomPasswordResetForm(request.POST)

        if form.is_valid():
            form.save()

            return render(request, "authy/post_password_reset.html")

        else:
            form = CustomPasswordResetForm()

    context = {"form": form}

    return render(request, "authy/password_reset.html", context)
