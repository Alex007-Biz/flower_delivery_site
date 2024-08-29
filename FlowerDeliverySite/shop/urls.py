from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('new', views.new, name='page2'),
    path('about', views.about, name='page3'),
    path('contacts', views.contacts, name='page4'),
]