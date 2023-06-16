from django import forms
from django.forms import MultiWidget, SplitDateTimeWidget
from .models import Room, Category

from datetime import datetime


class ReservationForm(forms.Form):
    today = datetime.now()

    check_in = forms.DateTimeField(
        label="Check In", required=True,
        widget=SplitDateTimeWidget(
            date_format="%d/%m/%Y", time_format="%H:%M",
        ))
    check_out = forms.DateTimeField(
        label="Check Out", required=True,
        widget=SplitDateTimeWidget(
            date_format="%d/%m/%Y", time_format="%H:%M",
        ))
    phone_no = forms.CharField(max_length=15, widget=forms.NumberInput)


class RoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [
            (category.pk, category.category_name) for category in Category.objects.all()
        ]

    class Meta:
        model = Room
        fields = '__all__'
