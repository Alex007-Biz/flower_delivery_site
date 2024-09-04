from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)

    # Переопределяем группы и разрешения, чтобы избежать конфликтов
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Уникальное имя для обратной связи
        blank=True,
        help_text='Группы, к которым принадлежит этот пользователь. Пользователь получит все разрешения, '\
                  'предоставленные каждой из своих групп.',
        verbose_name='группы',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Уникальное имя для обратной связи
        blank=True,
        help_text='Конкретные разрешения для этого пользователя.',
        verbose_name='разрешения пользователя',
    )

    def __str__(self):
        return self.username

class Flower(models.Model):
    name = models.CharField('Название букета', max_length=100)
    description = models.TextField(default='Описание не указано')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='media/flowers/', null=True, blank=True)

    class Meta:
        verbose_name = 'Цветы'
        verbose_name_plural = 'Цветы'

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    flowers = models.ManyToManyField(Flower)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"