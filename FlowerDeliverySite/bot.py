import os
import django
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from asgiref.sync import sync_to_async

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDeliverySite.settings')
django.setup()

# установка переменной окружения и вызов django.setup() выполняются до любого другого
# импорта. Это важно!!!

# Этот импорт должен идти после django.setup():
from shop.models import Flower, Order, CustomUser

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем клавиатуру с кнопками
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/order"), KeyboardButton(text="/make_order")],
    ],
    resize_keyboard=True  # Чтобы клавиатура была компактной
)

# Шаги диалога для создания заказа
class OrderForm(StatesGroup):
    choosing_flower = State()
    entering_address = State()
    entering_comment = State()


# Функция для приветствия нового пользователя (при первом взаимодействии с ботом)
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Приветствую Вас, {message.from_user.full_name}! "
        f"\n Добро пожаловать в Магазин цветов Bernardo's Flowers!"
        f"\n Кликните по /order чтобы посмотреть ваш заказ."
        f"\n Или оформите новый заказ: /make_order.",
        reply_markup=menu_keyboard  # Отправляем меню с кнопками
    )


# Начало создания заказа, выбор цветка
@dp.message(Command('make_order'))
async def make_order(message: Message, state: FSMContext):
    flowers = await sync_to_async(list)(Flower.objects.all())

    if flowers:
        flowers_list = "\n".join([f"{flower.id}. {flower.name} - {flower.price}₽" for flower in flowers])
        await message.answer(f"Выберите цветы для заказа, отправив ID цветка из списка:\n{flowers_list}")
        await state.set_state(OrderForm.choosing_flower)
    else:
        await message.answer("Цветов пока нет в наличии.")


# Пользователь выбирает цветок по ID
@dp.message(OrderForm.choosing_flower)
async def choose_flower(message: Message, state: FSMContext):
    flower_id = int(message.text)
    flower = await sync_to_async(Flower.objects.get)(id=flower_id)

    if flower:
        await state.update_data(flower_id=flower_id)
        await message.answer(f"Вы выбрали {flower.name}. Теперь введите адрес доставки:")
        await state.set_state(OrderForm.entering_address)
    else:
        await message.answer("Цветок не найден. Попробуйте снова.")


# Пользователь вводит адрес доставки
@dp.message(OrderForm.entering_address)
async def enter_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Введите комментарий к заказу (если есть) или отправьте /skip для пропуска:")
    await state.set_state(OrderForm.entering_comment)


# Пользователь вводит комментарий или пропускает этот шаг
@dp.message(OrderForm.entering_comment)
async def enter_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)

    # Получаем сохраненные данные
    data = await state.get_data()
    flower_id = data.get('flower_id')
    address = data.get('address')
    comment = data.get('comment', '')

    # Пытаемся получить пользователя по telegram_id
    try:
        user = await sync_to_async(CustomUser.objects.get)(telegram_id=message.from_user.id)
    except CustomUser.DoesNotExist:
        # Если пользователь не найден, создаем его
        user = await sync_to_async(CustomUser.objects.create)(
            telegram_id=message.from_user.id,
            username=message.from_user.username or 'unknown',  # добавьте другие необходимые поля
            first_name=message.from_user.first_name or '',
            last_name=message.from_user.last_name or ''
        )

    # Создаем заказ
    order = await sync_to_async(Order.objects.create)(
        user=user,
        delivery_place=address,
        commentary=comment
    )

    # Добавляем цветок в заказ
    flower = await sync_to_async(Flower.objects.get)(id=flower_id)
    await sync_to_async(order.flowers.add)(flower)

    await message.answer(f"Ваш заказ был успешно создан! Номер заказа: {order.id}")
    await state.clear()


# Пропуск комментария
@dp.message(Command('skip'))
async def skip_comment(message: Message, state: FSMContext):
    await enter_comment(message, state)


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
            flowers_info += f"Название: {flower.name}\nЦена: {flower.price}₽"
            path_to_image = flower.image.path
            # print(f"Path to image: {path_to_image}")

        message_text = f"Ваш заказ №: {order.id}\n{flowers_info}\nЗаказ создан: {order.created_at.date()}"
        # print(message_text)

        await message.answer(f"{message_text}")

        # path_2 = 'shop/media/media/flowers/Rob3YgoHjz_GcBpfxY.jpg'
        photo = FSInputFile(path_to_image)
        await message.answer_photo(photo=photo, caption="Ваш букет!")

    else:
        await message.answer("Нет доступных заказов.")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запуск бота
    asyncio.run(main())