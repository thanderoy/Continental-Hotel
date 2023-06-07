from django.urls import path
from . import views


app_name = "hotel"


urlpatterns = [
    path("", views.RoomOfferingView, name="room_offering"),
    path("room/<id>", views.RoomDetailView, name="room_detail"),
    path("reservations/", views.ReservationListView, name="reservation_list"),
    path(
        "reservation/<id>", views.ReservationDetailView, name="reservation_detail"
    ),
]
