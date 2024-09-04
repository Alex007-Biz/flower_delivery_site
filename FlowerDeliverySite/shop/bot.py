import os
import django
import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from config import TOKEN

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDeliverySite.settings')
django.setup()

from shop.models import Order, Flower, CustomUser  # Импортируйте необходимые модели

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TELEGRAM_TOKEN = TOKEN

# Функция для старта бота
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте! Я бот магазина цветов.')


# Функция для обработки нового заказа
def new_order(update: Update, context: CallbackContext) -> None:
    # Здесь вы можете получить информацию о заказе из контекста или базы данных
    # Это пример, вам нужно будет адаптировать его под вашу логику
    order = Order.objects.last()  # Получим последний заказ (или создайте свою логику получения заказа)
    if order:
        # Соберем информацию о заказе
        flowers_info = ""
        for flower in order.flowers.all():
            flowers_info += f"Название: {flower.name}\nЦена: {flower.price}₽\n"

        message = f"Новый заказ:\n\n{flowers_info}\n\nДата создания: {order.created_at}\n"
        # Если у вас есть комментарий к заказу, добавьте его сюда
        # message += f"Комментарий: {order.comment}\n"  # Предполагается, что вы добавите поле комментария в модель Order

        # Отправка изображения с букета
        for flower in order.flowers.all():
            if flower.image:  # Если изображение есть
                context.bot.send_photo(chat_id=update.message.chat_id, photo=open(flower.image.path, 'rb'), caption=message)
            else:
                context.bot.send_message(chat_id=update.message.chat_id, text=message)
    else:
        update.message.reply_text("Нет доступных заказов.")

def main() -> None:
    # Создайте Updater и передайте ему ваш токен
    updater = Updater(TELEGRAM_TOKEN)

    # Получите диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # На команды /start и /new_order будут реагировать соответствующие функции
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("new_order", new_order))

    # Начинаем получать обновления
    updater.start_polling()

    # Запускаем бота
    updater.idle()

if __name__ == '__main__':
    main()