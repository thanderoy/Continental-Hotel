from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):

    context = {

    }
    return render(request, "authy/login.html", context)