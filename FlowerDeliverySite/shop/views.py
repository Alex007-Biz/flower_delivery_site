from django.shortcuts import render, redirect, get_object_or_404
from .models import Flower, Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    flowers = Flower.objects.all()
    return render(request, 'shop/index.html', {'flowers': flowers})


def new(request):
    return render(request, 'shop/new.html')

def about(request):
    return render(request, 'shop/about.html')

def contacts(request):
    return render(request, 'shop/contacts.html')


def order_view(request):
    if request.method == 'POST':
        flower_id = request.POST.get('flower_id')
        selected_flower = get_object_or_404(Flower, id=flower_id)
        return render(request, 'shop/order.html', {'selected_flower': selected_flower})

    # Если это GET-запрос, перенаправляем на главную страницу или другую логику
    return redirect('index')


def confirm_order(request):
    if request.method == 'POST':
        flower_ids = request.POST.getlist('flowers')
        flowers = Flower.objects.filter(id__in=flower_ids)

        # Обработка создания заказа
        order = Order.objects.create(user=request.user)  # Предполагается, что пользователь аутентифицирован
        order.flowers.set(flowers)  # Предполагается, что у вас есть связь many-to-many с цветами
        order.save()

        return render(request, 'shop/order_success.html', {'order_id': order.id})

    return redirect('index')  # Если это не POST-запрос, перенаправляем на главную страницу

