from django import forms

from .models import Order
from .models import OrderItem

class OrderForm(forms.ModelForm):
    

    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "address_line_1",
            "address_line_2",
            "mobile_no",
            "alternative_no",
            "state",
            "district",
            "city",
            "pin_code",
            "email",
        ]