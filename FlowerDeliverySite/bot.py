import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import django
from config import TOKEN
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from shop.models import CustomUser, Flower, Order  # Импорт моделей

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDeliverySite.settings')
django.setup()

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Command(BaseCommand):
    help = 'Описание вашего скрипта'
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Скрипт выполнен успешно!'))

@sync_to_async
def get_flowers():
    return list(Flower.objects.all())

@sync_to_async
def get_user(user_id):
    try:
        return CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
        return None

@sync_to_async
def create_order(user, delivery_info):
    order = Order.objects.create(user=user, **delivery_info)
    return order

@sync_to_async
def get_flower(flower_id):
    return Flower.objects.get(id=flower_id)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Добро пожаловать в Магазин цветов Bernardo's Flowers! Кликните по /order для совершения заказа.")

@dp.message(Command('order'))
async def order(message: Message):
    flowers = await get_flowers()  # Получаем цветы асинхронно
    flower_list = '\n'.join([f"{flower.id}: {flower.name} - {flower.price} руб." for flower in flowers])
    await message.answer(f"Доступные букеты:\n{flower_list}\n\nПожалуйста, вышлите ID интересующих букетов через запятую.")

@dp.message(F.text & ~F.command())
async def handle_message(message: Message):
    user_id = message.from_user.id  # Получаем ID пользователя Telegram
    flower_ids = message.text.split(',')

    # Запрашиваем дополнительнуюинформацию о заказе
    await message.answer("Пожалуйста, введите дату, время и место доставки через запятую (например, 2023-10-10, 12:00, ул. Ленина 1).")

    # Ожидаем следующего сообщения от пользователя
@dp.message(F.text & ~F.command())
async def handle_delivery_info(delivery_message: Message):
    delivery_info = delivery_message.text.split(',')
    if len(delivery_info) < 3:
        await delivery_message.answer("Пожалуйста, укажите дату, время и место доставки.")
        return

        date, time, address = map(str.strip, delivery_info)

        # Получаем пользователя
    user = await get_user(user_id)
    if not user:
        await delivery_message.answer("Пользователь не найден. Попробуйте позже.")
        return

    order = await create_order(user, {'date': date, 'time': time, 'address': address})

    for flower_id in flower_ids:
        try:
            flower = await get_flower(int(flower_id.strip()))  # Получаем цветок асинхронно
            order.flowers.add(flower)
        except Flower.DoesNotExist:
            await delivery_message.answer(f"Букет №{flower_id.strip()} не существует.")
            logger.error(f"Букет с ID {flower_id.strip()} не найден.")

    await delivery_message.answer(f'Ваш заказ оформлен!\nДоставка:\nДата: {date}\nВремя: {time}\nАдрес: {address}')

    # Вызываем функцию для обработки информации о доставке
    await handle_delivery_info(message)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())