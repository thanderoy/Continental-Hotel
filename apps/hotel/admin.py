from django.contrib import admin
from .models import Reservation, Room, Category
from .forms import RoomForm


class RoomAdmin(admin.ModelAdmin):
    form = RoomForm


admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation)
admin.site.register(Category)
