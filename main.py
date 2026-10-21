import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8976663011:AAGjQuunbt2H1hUS4zpM3YAIatwJZ340uj4" # Лучше поменять на новый!
ADMIN_URL = "https://t.me/Hwoqpi"

# --- ТЕКСТЫ МАГАЗИНА ---
SHOP_TEXT = (
    "🛍 <b>Магазин ASTRALDLС</b>\n\n"
    "Вход в приват: 1000 Stars\n"
    "Зенин + Рут + iOS: 500 Stars\n"
    "Зенин: 200 Stars\n"
    "Нон-Рут: 15 Stars\n"
    "Кламси: Free\n"
    "Рут права: 50 Stars\n"
    "Анти-бан: 50 Stars\n"
    "Промт: 25 Stars\n\n"
    "👇 <b>Наш собственный чит Astraldlc:</b>"
)

FREE_TEXT = "🟢 <b>Astraldlc FREE</b>\n\nБазовые функции на бесплатной основе.\n📥 Скачать и узнать подробности: @Hwoqpi"
PREMIUM_TEXT = "💎 <b>Astraldlc PREMIUM</b>\n\n🔥 Полный доступ ко всем функциям!\n🛡 Улучшенный обход анти-чита.\n📩 Для покупки пиши: @Hwoqpi"
DEV_TEXT = "⏳ <b>Astraldlc (В разработке)</b>\n\nМы работаем над новыми функциями. Совсем скоро будет крутое обновление! 🚀"
SUPPORT_TEXT = "💬 <b>Поддержка ASTRALDLС</b>\n\nПо всем вопросам пиши: @Hwoqpi"

logging.basicConfig(level=logging.INFO)
router = Router()

# --- КЛАВИАТУРЫ ---
def main_menu_kb():
    # Главное меню с кнопками Магазин и Поддержка
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Магазин", callback_data="shop"),
            InlineKeyboardButton(text="💬 Поддержка", callback_data="support")
        ]
    ])

def shop_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Astraldlc Free", callback_data="free")],
        [InlineKeyboardButton(text="💎 Astraldlc Premium", callback_data="premium")],
        [InlineKeyboardButton(text="⏳ В разработке", callback_data="dev")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        [InlineKeyboardButton(text="✍️ Написать админу", url=ADMIN_URL)]
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back")]
    ])

# --- ОБРАБОТЧИКИ ---

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 <b>Добро пожаловать в ASTRALDLС!</b>\n\n"
        "Выбери действие в меню ниже:",
        reply_markup=main_menu_kb()
    )

@router.callback_query(F.data == "shop")
async def cb_shop(call: CallbackQuery):
    await call.message.edit_text(SHOP_TEXT, reply_markup=shop_kb())
    await call.answer()

@router.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery):
    await call.message.edit_text(SUPPORT_TEXT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "free")
async def cb_free(call: CallbackQuery):
    await call.message.edit_text(FREE_TEXT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "premium")
async def cb_premium(call: CallbackQuery):
    await call.message.edit_text(PREMIUM_TEXT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "dev")
async def cb_dev(call: CallbackQuery):
    await call.message.edit_text(DEV_TEXT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "back")
async def cb_back(call: CallbackQuery):
    await call.message.edit_text(
        "👋 <b>Добро пожаловать в ASTRALDLС!</b>\n\n"
        "Выбери действие в меню ниже:",
        reply_markup=main_menu_kb()
    )
    await call.answer()

# --- УМНЫЙ ОТВЕТ НА ЛЮБЫЕ ВОПРОСЫ ---
@router.message()
async def echo(message: Message):
    text = message.text.lower()
    
    # Бот пытается распознать ключевые слова
    if "цена" in text or "прайс" in text or "почём" in text or "сколько" in text:
        await message.answer("💰 Актуальный прайс-лист ты можешь посмотреть в разделе <b>🛒 Магазин</b>!", reply_markup=main_menu_kb())
    elif "купить" in text or "оплата" in text or "оплатить" in text:
        await message.answer("💳 Для покупки напиши напрямую админу: @Hwoqpi", reply_markup=main_menu_kb())
    elif "рут" in text or "root" in text:
        await message.answer("🛡 У нас есть как Рут, так и Нон-Рут версии. Подробности в магазине!", reply_markup=main_menu_kb())
    elif "привет" in text or "здравствуйте" in text or "хай" in text:
        await message.answer("👋 Привет! Чем я могу помочь? Нажми на кнопку ниже или напиши свой вопрос.", reply_markup=main_menu_kb())
    else:
        # Если бот не понял, он переводит на админа
        await message.answer(
            "🤖 Я пока не знаю ответа на этот вопрос, но мой создатель точно знает!\n\n"
            "Напиши ему напрямую: @Hwoqpi\n"
            "Или выбери действие в меню:",
            reply_markup=main_menu_kb()
        )

# --- СЕРВЕР ДЛЯ RENDER ---
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
    await start_web()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
