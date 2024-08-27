import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import requests
import django
from config import TOKEN
from asgiref.sync import sync_to_async


# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDeliverySite.settings')
# print("Before Django setup")
django.setup()
# print("Django setup complete")

# Импорт моделей после настройки Django
from shop.models import Flower, Order

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@sync_to_async
def get_flowers():
    return list(Flower.objects.all())

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Добро пожаловать на Flower Delivery Service! Кликните по /order для совершения заказа.')

@dp.message(Command('order'))
async def order(message: Message):
    flowers = await get_flowers()  # Получаем цветы асинхронно
    flower_list = '\n'.join([f"{flower.id}: {flower.name} - ${flower.price}" for flower in flowers])
    await message.answer(f"Доступные букеты:\n{flower_list}\n\nПожалуйста вышлите ID интересующих букетов через запятую.")

@dp.message(F.text & ~F.command())
async def handle_message(message: Message):
    text = message.text.split(',')
    flower_ids = [int(id.strip()) for id in text if id.strip().isdigit()]
    user_id = message.from_user.id  # Get the Telegram user ID

    # Create an order using the Telegram user ID
    order = Order.objects.create(user_id=user_id)  # Make sure that user_id matches your User model

    for flower_id in flower_ids:
        try:
            flower = Flower.objects.get(id=flower_id)
            order.flowers.add(flower)
        except Flower.DoesNotExist:
            await message.answer(f"Flower with ID {flower_id} does not exist.")

    await message.answer('Your order has been placed!')

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())


# async def on_startup(dp: Dispatcher):
#     logging.info("Starting bot...")
#
# if __name__ == '__main__':
#     from aiogram import executor
#
#     # Запуск бота
#     executor.start_polling(dp, on_startup=on_startup, skip_updates=True)