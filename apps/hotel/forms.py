from django import forms
from .models import Room, Category

from datetime import datetime


class ReservationForm(forms.Form):
    today = datetime.now()
    date_input = ["%m/%d/%Y %H:%M"]

    check_in = forms.DateTimeField(
        label="Check In", input_formats=date_input, required=True,
        widget=forms.DateTimeInput)
    check_out = forms.DateTimeField(
        label="Check Out", input_formats=date_input, required=True,
        widget=forms.DateTimeInput)
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
