import os
import django
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDeliverySite.settings')
django.setup()

from shop.models import Order  # Импортируйте необходимые модели

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TELEGRAM_TOKEN = TOKEN

# Функция для старта бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Здравствуйте! Я бот магазина цветов.')

# Функция для обработки нового заказа
async def new_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    order = Order.objects.last()  # Получим последний заказ (или создайте свою логику получения заказа)
    if order:
        # Соберем информацию о заказе
        flowers_info = ""
        for flower in order.flowers.all():
            flowers_info += f"Название: {flower.name}\nЦена: {flower.price}₽\n"

        message = f"Новый заказ:\n\n{flowers_info}\n\nДата создания: {order.created_at}\n"

        # Отправка изображения с букета
        for flower in order.flowers.all():
            if flower.image:  # Если изображение есть
                await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(flower.image.path, 'rb'), caption=message)
            else:
                await context.bot.send_message(chat_id=update.message.chat_id, text=message)
    else:
        await update.message.reply_text("Нет доступных заказов.")

async def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # На команды /start и /new_order будут реагировать соответствующие функции
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new_order", new_order))

    # Начинаем получать обновления
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())