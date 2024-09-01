from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='page2'),
    path('about/', views.about, name='page3'),
    path('contacts/', views.contacts, name='page4'),
    path('order/', views.order, name='order'),  # Для общего заказа
    path('order/<int:flower_id>/', views.order, name='order_with_flower'),  # Для заказа конкретного цветка
]

