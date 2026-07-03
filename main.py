import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN
from api import get_crypto_price
from parser import fetch_news
from weather import get_weather
from earthquake import get_earthquakes

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я крипто-бот с расширенными возможностями.\n"
        "/price <монета> — цена с CoinGecko (напр. /price bitcoin)\n"
        "/news — последние новости CoinDesk\n"
        "/weather <город> — погода (напр. /weather Moscow)\n"
        "/earthquake [мин. магнитуда] — последние землетрясения (по умолч. 4.0)\n"
        "   Пример: /earthquake 5.5"
    )

@dp.message(Command("price"))
async def cmd_price(message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply("Укажи монету: /price bitcoin")
        return
    coin = args[1].lower()
    result = await get_crypto_price(coin)
    await message.reply(result)

@dp.message(Command("news"))
async def cmd_news(message: Message):
    await message.answer("Собираю новости...")
    news_text = await fetch_news(limit=5)
    await message.reply(news_text, disable_web_page_preview=True)

@dp.message(Command("weather"))
async def cmd_weather(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Укажи город: /weather Москва")
        return
    city = args[1].strip()
    await message.answer("Запрашиваю погоду...")
    result = await get_weather(city)
    await message.reply(result)

@dp.message(Command("earthquake", "eq"))
async def cmd_earthquake(message: Message):
    args = message.text.split()
    min_mag = 4.0
    if len(args) > 1:
        try:
            min_mag = float(args[1])
        except ValueError:
            await message.reply("Неверная магнитуда, используй число (например, 5.0)")
            return
    await message.answer(f"Ищу землетрясения с магнитудой ≥ {min_mag}...")
    result = await get_earthquakes(min_mag)
    await message.reply(result)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())