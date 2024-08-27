import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDeliverySite.settings')
django.setup()

from shop.models import Flower, Order

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = '7183754748:AAG-1AUzjUj934nPRdib4gyJp7pjgauQWs8'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply('Welcome to the Flower Delivery Service! Use /order to make an order.')

@dp.message(Command("order"))
async def order(message: types.Message):
    flowers = Flower.objects.all()
    flower_list = '\n'.join([f"{flower.id}: {flower.name} - ${flower.price}" for flower in flowers])
    await message.reply(f"Available flowers:\n{flower_list}\n\nPlease send the flower IDs separated by commas.")

@dp.message(F.text & ~F.command())
async def handle_message(message: types.Message):
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
            await message.reply(f"Flower with ID {flower_id} does not exist.")

    await message.reply('Your order has been placed!')

async def on_startup(dp: Dispatcher):
    logging.info("Starting bot...")

if __name__ == '__main__':
    from aiogram import executor

    # Запуск бота
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)