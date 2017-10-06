from django import forms
from .models import *


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['url', 'email']
# Create your tests here.
