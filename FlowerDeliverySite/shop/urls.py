from django.urls import path
from . import views  # Импортируйте ваши представления
from .views import order_view, confirm_order
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('new/', views.new, name='page2'),
    path('about/', views.about, name='page3'),
    path('contacts/', views.contacts, name='page4'),
    path('order/', order_view, name='order_view'),
    path('confirm_order/', confirm_order, name='confirm_order'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup'),  # Добавьте этот маршрут
]

