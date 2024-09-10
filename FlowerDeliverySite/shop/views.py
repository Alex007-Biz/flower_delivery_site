from django.shortcuts import render, redirect, get_object_or_404
from .models import Flower, Order, CustomUser
from .forms import  CustomUserCreationForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()
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

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Сохраняем пользователя, но не отправляем в БД пока
            user.telegram_id = form.cleaned_data.get('telegram_id')  # Получаем telegram_id из формы
            user.set_password(form.cleaned_data['password'])
            user.save()  # Теперь сохраняем пользователя с telegram_id
            return redirect('login')  # или куда-то еще после успешной регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

@login_required
def confirm_order(request):
    if request.method == 'POST':
        flower_ids = request.POST.getlist('flowers')
        flowers = Flower.objects.filter(id__in=flower_ids)
        # Получаем экземпляр CustomUser
        custom_user = CustomUser.objects.get(username=request.user.username)
        if not flowers:
        # Обработка ошибки: нет выбранных цветов
            return render(request, 'shop/order.html', {'error': 'Выберите хотя бы один цветок.'})
        # Извлечение данных из формы
        delivery_place = request.POST.get('delivery_place')
        delivery_date = request.POST.get('delivery_date')
        commentary = request.POST.get('commentary')

        # Обработка создания заказа
        order = Order.objects.create(user=custom_user,
                                     delivery_place=delivery_place,
                                     delivery_date=delivery_date,
                                     commentary=commentary) # Передаем дополнительные данные
        order.flowers.set(flowers)  # Предполагается, что у вас есть связь many-to-many с цветами
        order.save()
        # Извлекаем выбранные цветы из заказа
        selected_flowers = order.flowers.all()  # Получаем все цветы, связанные с заказом
        # Вычисляем общую сумму
        total_sum = sum(flower.price for flower in selected_flowers)

        return render(request, 'shop/order_success.html', {
            'order_id': order.id,
            'selected_flowers': selected_flowers,
            'total_sum': total_sum,  # Передаем общую сумму в контекст
            'delivery_place': delivery_place,
            'delivery_date': delivery_date,
            'commentary': commentary
        })

    return redirect('index')  # Если это не POST-запрос, перенаправляем на главную страницу

