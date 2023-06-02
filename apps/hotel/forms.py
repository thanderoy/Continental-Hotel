from django import forms
from datetime import datetime


class ReservationForm(forms.Form):

    today = datetime.now()

    check_in = forms.DateTimeField(input_formats=["%m/%d/%Y %H:%M"], required=True)
    check_out = forms.DateTimeField(input_formats=["%m/%d/%Y %H:%M"], required=True)
    phone_no = forms.CharField(max_length=15)
