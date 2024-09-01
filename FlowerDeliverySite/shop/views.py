from django.shortcuts import render, redirect
from .models import Flower, Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def index(request):
    flowers = Flower.objects.all()
    return render(request, 'shop/index.html', {'flowers': flowers})
    # return render(request, 'shop/index.html')


def new(request):
    return render(request, 'shop/new.html')
    # return HttpResponse("<h1>Это вторая страница проекта на Django</h1>")

def about(request):
    return render(request, 'shop/about.html')

def contacts(request):
    return render(request, 'shop/contacts.html')

# @login_required
def order(request):
    if request.method == 'POST':
        flower_ids = request.POST.getlist('flowers')
        order = Order.objects.create(user=request.user)
        order.flowers.add(*flower_ids)
        return redirect('index')
    flowers = Flower.objects.all()
    return render(request, 'shop/order.html', {'flowers': flowers})