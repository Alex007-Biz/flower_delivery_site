import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import os


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/photo\n/photo2")

@dp.message(Command('photo'))
async def photo(message: Message):
    rand_photo = 'photo3.jpg'
    if os.path.exists(rand_photo):  # Проверяем, существует ли файл
        # with open(rand_photo, 'rb') as file:  # Открываем файл в бинарном режиме
        photo_file = FSInputFile(rand_photo)
        await message.answer_photo(photo=photo_file, caption='Это супер крутая картинка')
    else:
        await message.answer("Файл не найден!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# @dp.message(Command('photo2'))
# async def photo2(message: Message):
#     rand_photo = 'https://i06.fotocdn.net/s205/94a92d5ade84ce23/public_pin_l/2362727257.jpg'
#     await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')