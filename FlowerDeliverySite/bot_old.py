import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters  # Импортируем Filters из filters
from django.conf import settings
from django.utils import translation
import django
import logging

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDeliverySite.settings')
django.setup()

from shop.models import Flower, Order

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to the Flower Delivery Service! Use /order to make an order.')

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    flowers = Flower.objects.all()
    flower_list = '\n'.join([f"{flower.id}: {flower.name} - ${flower.price}" for flower in flowers])
    await update.message.reply_text(f"Available flowers:\n{flower_list}\n\nPlease send the flower IDs separated by commas.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.split(',')
    flower_ids = [int(id.strip()) for id in text]
    user = update.message.from_user
    order = Order.objects.create(user=user)

    for flower_id in flower_ids:
        flower = Flower.objects.get(id=flower_id)
        order.flowers.add(flower)

    await update.message.reply_text('Your order has been placed!')

def main() -> None:
    application = ApplicationBuilder().token("7183754748:AAG-1AUzjUj934nPRdib4gyJp7pjgauQWs8").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("order", order))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()