from django.shortcuts import render, redirect
from .models import Flower, Order
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    flowers = Flower.objects.all()
    return render(request, 'shop/index.html', {'flowers': flowers})

@login_required
def order(request):
    if request.method == 'POST':
        flower_ids = request.POST.getlist('flowers')
        order = Order.objects.create(user=request.user)
        order.flowers.add(*flower_ids)
        return redirect('index')
    flowers = Flower.objects.all()
    return render(request, 'shop/order.html', {'flowers': flowers})