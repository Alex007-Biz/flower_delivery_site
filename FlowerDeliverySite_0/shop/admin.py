from django.contrib import admin
from .models import Flower, Order, CustomUser

# Register your models here.
admin.site.register(Flower)
admin.site.register(Order)
admin.site.register(CustomUser)
