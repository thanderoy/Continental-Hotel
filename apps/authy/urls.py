from django.urls import path
from . import views


app_name = "authy"


urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("password_reset/", views.password_reset, name="password_reset"),
]
