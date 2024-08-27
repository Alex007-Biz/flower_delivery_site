from django.shortcuts import render, redirect
from .models import Flower, Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def index(request):
    flowers = Flower.objects.all()
    return HttpResponse("<h1>Это магазин цветов!</h1>")
    return render(request, 'shop/index.html', {'flowers': flowers})

def new(request):
    return HttpResponse("<h1>Это втоggя страница проекта на Django</h1>")

def new_n(request):
    return HttpResponse("<h1>Это третья страница проекта на Django</h1>")

@login_required
def order(request):
    if request.method == 'POST':
        flower_ids = request.POST.getlist('flowers')
        order = Order.objects.create(user=request.user)
        order.flowers.add(*flower_ids)
        return redirect('index')
    flowers = Flower.objects.all()
    return render(request, 'shop/order.html', {'flowers': flowers})