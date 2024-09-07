import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN



bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/photo")

@dp.message(Command('photo'))
async def photo(message: Message):
    rand_photo = 'E:\Алексей\Github\flower_delivery_site\FlowerDeliverySite\shop\media\media\flowers\51-roza-fridom-6.webp'
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())