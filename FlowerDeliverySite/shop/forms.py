from .models import Order, CustomUser
from django import forms
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from django.contrib.auth.forms import UserCreationForm

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['user']

class CustomUserCreationForm(forms.ModelForm):
	telegram_id = forms.IntegerField(required=False)  # Добавляем поле telegram_id
	class Meta:
		model = CustomUser
		fields = ('username', 'email', 'password', 'telegram_id')
