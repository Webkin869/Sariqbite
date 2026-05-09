from django import forms
from .models import Order


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    phone = forms.CharField(max_length=30)
    address = forms.CharField(max_length=255)
    note = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)
    payment_method = forms.ChoiceField(choices=Order.PaymentMethod.choices)
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    distance_km = forms.FloatField(required=False, min_value=0)
