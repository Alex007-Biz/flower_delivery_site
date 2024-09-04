from .models import Order
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['user']
