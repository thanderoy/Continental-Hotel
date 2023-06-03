from django.urls import path
from . import views


app_name = "hotel"


urlpatterns = [
    path(
        "reservation/<int: id>", views.ReservationDetailView, name="reservation_detail"
    ),
]
