import os
import django
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputFile
from config import TOKEN
from asgiref.sync import sync_to_async

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDeliverySite.settings')
django.setup()

from shop.models import Order  # Импортируйте необходимые модели

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для старта бота
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Добро пожаловать в Магазин цветов Bernardo's Flowers! Кликните по /order для совершения заказа."
    )

# Функция для обработки нового заказа
@dp.message(Command('order'))
async def order(message: Message):
    # Получаем последний заказ
    order = await sync_to_async(Order.objects.last)()

    if order:
        # Соберем информацию о заказе
        flowers_info = ""
        flowers = await sync_to_async(list)(order.flowers.all())  # Получаем все цветы асинхронно

        for flower in flowers:
            flowers_info += f"Название: {flower.name}\nЦена: {flower.price}₽\n"

        message_text = f"Новый заказ:\n{flowers_info}\nДата создания: {order.created_at}\n"
        print(message_text)

        await message.answer(
            f"Ваш заказ: {message_text}."
        )

        # Отправка изображения с букета
        # for flower in flowers:
        #     if flower.image:  # Если изображение есть
        #         print(f"Path to image: {flower.image.path}")
        #         # Создаем InputFile из пути к изображению
        #         with open(flower.image.path, 'rb') as file:
        #             photo = InputFile(file)
        #         # photo = InputFile(flower.image.path)
        #         await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=message_text)
        #     else:
        #         await bot.send_message(chat_id=message.chat.id, text=message_text)
    else:
        await message.answer("Нет доступных заказов.")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запуск бота
    asyncio.run(main())