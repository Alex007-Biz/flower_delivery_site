from django.urls import path
from . import views
from .views import order_view, confirm_order

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='page2'),
    path('about/', views.about, name='page3'),
    path('contacts/', views.contacts, name='page4'),
    path('order/', order_view, name='order_view'),
    path('confirm_order/', confirm_order, name='confirm_order'),
    # path('order/<int:flower_id>/', views.order, name='order_with_flower'),  # Для заказа конкретного цветка
]

