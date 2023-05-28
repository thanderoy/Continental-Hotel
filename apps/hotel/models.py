from django.db import models
from django.conf import settings

USER_MODEL = settings.AUTH_USER_MODEL


ROOM_CATEGORIES = (
    ("BZS", "BUSINESS SUITE"),
    ("TWS", "TWIN SUITE"),
    ("EXS", "EXECUTIVE SUITE"),
    ("SGB", "SINGLE BED"),
)

RESERVATION_STATUS = (
    ("PENDING", "Pending"),
    ("FULFILLED", "Fulfilled"),
    ("CANCELLED", "Cancelled"),
)


class Room(models.Model):
    room_number = models.IntegerField()
    category = models.CharField(choices=ROOM_CATEGORIES, max_length=3)
    beds = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=1000, null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return (
            f"{self.room_number} {self.category}: "
            f"{self.beds} Bed(s) - {self.price}"
        )


class Reservation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name='reservations'
    )
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    status = models.BooleanField(
        max_length=50, choices=RESERVATION_STATUS, default="Pending"
    )

    def __str__(self) -> str:
        return (
            f"{self.room.room_number} {self.room.category} -> "
            f"{self.owner} ({self.check_in} - {self.check_out})"
        )

    @property
    def room_category(self) -> str:
        return self.room.category

    def cancel(self) -> None:
        """
        Cancels a reservation.
        """
        self.status = "CANCELLED"
        self.save()
