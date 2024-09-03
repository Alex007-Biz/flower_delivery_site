import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import django
from config import TOKEN
from asgiref.sync import sync_to_async

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDeliverySite.settings')
django.setup()

# Импорт моделей после настройки Django
from shop.models import Flower, Order, CustomUser  # Не забудьте импортировать User

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@sync_to_async
def get_flowers():
    return list(Flower.objects.all())

@sync_to_async
def get_user(user_id):
    return CustomUser.objects.get(id=user_id)

@sync_to_async
def create_order(user):
    return Order.objects.create(user=user)

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
    await message.answer(f"Доступные букеты:\n{flower_list}\n\nПожалуйста вышлите ID интересующих букетов через запятую.")

@dp.message(F.text & ~F.command())
async def handle_message(message: Message):
    text = message.text.split(',')
    flower_ids = [int(id.strip()) for id in text if id.strip().isdigit()]
    user_id = message.from_user.id  # Получаем ID пользователя Telegram

    try:
        # Получаем пользователя из базы данных
        user = await get_user(user_id)  # Используем await здесь
    except User.DoesNotExist:
        await message.answer("Пользователь не найден. Попробуйте позже.")
        logger.error(f"Пользователь с ID {user_id} не найден.")
        return
    try:
        order = await create_order(user)  # Используем await здесь
        for flower_id in flower_ids:
            try:
                flower = await get_flower(flower_id)  # Получаем цветок асинхронно
                order.flowers.add(flower)
            except Flower.DoesNotExist:
                await message.answer(f"Букет №{flower_id} не существует.")
                logger.error(f"Букет с ID {flower_id} не найден.")

        await message.answer('Ваш заказ уже собирается!')

    except Exception as e:
        logger.error(f"Ошибка при создании заказа: {e}")
        await message.answer("Произошла ошибка при оформлении вашего заказа. Попробуйте позже.")

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())