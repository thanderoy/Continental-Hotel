from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet

from apps.common.models import BaseModel

USER_MODEL = settings.AUTH_USER_MODEL


class Category(BaseModel):
    category_code = models.CharField(max_length=3)
    category_name = models.CharField(max_length=50)
    beds = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.category_name} [{self.category_code}] \
        - Price: {self.price}"

    def get_rooms(self) -> QuerySet[Room]:
        """
        Returns all rooms in specific category.
        """
        return Room.objects.filter(
            category=self
        )

    def get_rooms_available(self) -> QuerySet[Room]:
        """
        Returns all available rooms in specific category.
        """
        return self.get_rooms().filter(
            is_available=True
        )


class Room(BaseModel):
    room_number = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return (
            f"Room {self.room_number} {self.category.category_name} \
            - {self.category.price}"
        )


class ReservationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    FULFILLED = "FULFILLED", "Fulfilled"
    CANCELLED = "CANCELLED", "Cancelled"


class Reservation(BaseModel):
    owner = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="reservations"
    )
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    status = models.BooleanField(
        max_length=50, choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING
    )

    def __str__(self) -> str:
        return (
            f"{self.room.room_number} {self.room.category} -> \
            {self.owner} ({self.check_in} - {self.check_out})"
        )

    @property
    def room_category(self) -> str:
        return self.room.category.category_name

    def cancel(self) -> None:
        """
        Cancels a reservation.
        """
        self.status = ReservationStatus.CANCELLED
        self.save()
