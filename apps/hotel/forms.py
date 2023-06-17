from django import forms
from .models import Room, Category, Reservation

from datetime import datetime


class ReservationForm(forms.ModelForm):
    today = datetime.now()

    check_in = forms.DateTimeField(
        label="Check In", required=True, widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control"
            }
        ))
    check_out = forms.DateTimeField(
        label="Check Out", required=True, widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control"
            }
        ))
    # phone_no = forms.CharField(max_length=15, widget=forms.NumberInput)

    class Meta:
        model = Reservation
        fields = ("check_in", "check_out")


class CancelReservationForm(forms.Form):

    class Meta:
        model = Reservation


class RoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [
            (category.pk, category.category_name) for category in Category.objects.all()
        ]

    class Meta:
        model = Room
        fields = '__all__'
