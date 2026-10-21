import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8976663011:AAGjQuunbt2H1hUS4zpM3YAIatwJZ340uj4"
ADMIN_URL = "https://t.me/Hwoqpi"

SHOP_TEXT = (
    "🛍 Магазин ASTRALDLС\n\n"
    "Вход в приват: 1000 Stars\n"
    "Зенин + Рут + iOS: 500 Stars\n"
    "Зенин: 200 Stars\n"
    "Нон-Рут: 15 Stars\n"
    "Кламси: Free\n"
    "Рут права: 50 Stars\n"
    "Анти-бан: 50 Stars\n"
    "Промт: 25 Stars\n\n"
    "❗️ Ещё товары в ЛС: @Hwoqpi"
)

SUPPORT_TEXT = "💬 Поддержка ASTRALDLС\n\nПо всем вопросам пиши: @Hwoqpi"

logging.basicConfig(level=logging.INFO)
router = Router()

def get_admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Написать админу", url=ADMIN_URL)]
    ])

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("👋 Добро пожаловать в <b>ASTRALDLС</b>!\n\nВыбери действие в меню слева или напиши /shop.")

@router.message(Command("shop"))
@router.message(F.text == "🛒 Магазин")
async def cmd_shop(message: Message):
    await message.answer(SHOP_TEXT, reply_markup=get_admin_kb())

@router.message(Command("support"))
@router.message(F.text == "💬 Поддержка")
async def cmd_support(message: Message):
    await message.answer(SUPPORT_TEXT, reply_markup=get_admin_kb())

# --- Мини-сервер для Render (обманка) ---
async def health(request):
    return web.Response(text="Bot is alive")

async def start_web():
    app = web.Application()
    app.router.add_get('/', health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

async def main():
    await start_web()  # Запускаем фейковый сайт
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
