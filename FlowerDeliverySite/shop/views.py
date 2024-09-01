from django.shortcuts import render, redirect, get_object_or_404
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
        flower_id = request.POST.get('flower_id')
        flower = get_object_or_404(Flower, id=flower_id)
        return render(request, 'shop/order.html', {'flowers': [flower]})
        # Передаем только выбранный цветок
        # Если GET-запрос, вы можете вернуть пустую страницу или список всех цветов (если это необходимо)
        flowers = Flower.objects.all()
        return render(request, 'shop/order.html', {'flowers': flowers})

    #     order = Order.objects.create(user=request.user)
    #     order.flowers.add(*flower_ids)
    #     return redirect('index')
    # flowers = Flower.objects.all()
    # return render(request, 'shop/order.html', {'flowers': flowers})