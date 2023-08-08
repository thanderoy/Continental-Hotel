from __future__ import annotations
from django.utils import timezone

from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet

from apps.common.models import BaseModel
from .helpers import ReservationException

USER_MODEL = settings.AUTH_USER_MODEL


class Category(BaseModel):
    category_code = models.CharField(max_length=3)
    category_name = models.CharField(max_length=50)
    beds = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_file = models.ImageField(upload_to="images/category/", null=True)

    def __str__(self) -> str:
        return f"{self.category_name} [{self.category_code}] \
        - Price: {self.price}"

    def get_rooms(self) -> QuerySet[Room]:
        """
        Returns all rooms in specific category.
        """
        return Room.objects.filter(category=self)

    def get_rooms_available(self) -> QuerySet[Room]:
        """
        Returns all available rooms in specific category.
        """
        return self.get_rooms().filter(is_available=True)


class Room(BaseModel):
    room_number = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Room {self.room_number} {self.category.category_name} \
            - {self.category.price}"

    def reserve(self, owner, check_in, check_out):
        if not self.is_available:
            raise ReservationException(f"Room {self.room_number} is already reserved")

        try:
            reservation = Reservation.objects.create(
                owner=owner,
                room=self,
                check_in=check_in,
                check_out=check_out,
                status=ReservationStatus.PENDING,
            )

            self.is_available = False
            self.save()

            return reservation
        except Exception as e:
            print(e)
            return None


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
    status = models.CharField(
        max_length=50,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING,
    )
    cancellation_date = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self) -> str:
        return f"{self.room.room_number} {self.room.category} -> \
            {self.owner} ({self.check_in} - {self.check_out})"

    @property
    def room_category(self) -> str:
        return self.room.category.category_name

    def cancel(self) -> None:
        """
        Cancels a reservation.
        """
        self.status = ReservationStatus.CANCELLED
        self.room.is_available = True
        self.cancellation_date = timezone.now()
        self.room.save()
        self.save()
