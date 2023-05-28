from django.contrib import admin
from .models import Reservation, Room

admin.site.register(Room)
admin.site.register(Reservation)
