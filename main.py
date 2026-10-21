import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

BOT_TOKEN = "8976663011:AAGjQuunbt2H1hUS4zpM3YAIatwJZ340uj4" # Лучше поменять на новый!
ADMIN_URL = "https://t.me/Hwoqpi"

# --- ТЕКСТЫ ---
START_TEXT = "👋 <b>Добро пожаловать в ASTRALDLС!</b>\n\nВыбери действие в меню:"
SHOP_TEXT = "🛍 <b>Магазин ASTRALDLС</b>\n\nВыбери нужный товар из списка ниже 👇\n\n💡 <i>Наш собственный чит Astraldlc:</i>"
SUPPORT_TEXT = "💬 <b>Поддержка ASTRALDLС</b>\n\nПо всем вопросам пиши: @Hwoqpi"

# Тексты для софта
FREE_TEXT = "🟢 <b>Astraldlc FREE</b>\n\nБазовые функции на бесплатной основе.\n📥 Скачать и узнать подробности: @Hwoqpi"
PREMIUM_TEXT = "💎 <b>Astraldlc PREMIUM</b>\n\n🔥 Полный доступ ко всем функциям!\n🛡 Улучшенный обход анти-чита.\n📩 Для покупки пиши: @Hwoqpi"
DEV_TEXT = "⏳ <b>Astraldlc (В разработке)</b>\n\nМы работаем над новыми функциями. Совсем скоро будет крутое обновление! 🚀"

# Тексты для товаров Standoff 2
TEXT_PRIVAT = "🔒 <b>Вход в приват</b>\n\nЦена: <b>1000 Stars</b>\nДоступ к закрытым функциям и приватному софту."
TEXT_ZENIN_RUT = "👑 <b>Зенин + Рут + iOS</b>\n\nЦена: <b>500 Stars</b>\nПолный фарш: Зенин, Рут права и поддержка iOS."
TEXT_ZENIN = "🧠 <b>Зенин</b>\n\nЦена: <b>200 Stars</b>\nЛегендарный чит Зенин для комфортной игры."
TEXT_NON_RUT = "🔓 <b>Нон-Рут</b>\n\nЦена: <b>15 Stars</b>\nБыстрый и безопасный софт без рут-прав."
TEXT_KLAMSI = "🎁 <b>Кламси</b>\n\nЦена: <b>FREE</b>\nБесплатный софт для старта."
TEXT_ROOT = "🛡 <b>Рут права</b>\n\nЦена: <b>50 Stars</b>\nПолучение прав суперпользователя на устройстве."
TEXT_ANTIBAN = "🚫 <b>Анти-бан</b>\n\nЦена: <b>50 Stars</b>\nЗащита вашего аккаунта от блокировок."
TEXT_PROMPT = "📝 <b>Промт</b>\n\nЦена: <b>25 Stars</b>\nСпециальный промт для обхода проверок."

logging.basicConfig(level=logging.INFO)
router = Router()

# --- КЛАВИАТУРЫ ---
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 МАГАЗИН", callback_data="shop"),
         InlineKeyboardButton(text="💬 ПОДДЕРЖКА", callback_data="support")]
    ])

def shop_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        # Товары
        [InlineKeyboardButton(text="🔒 Вход в приват | 1000🌟", callback_data="priv")],
        [InlineKeyboardButton(text="👑 Зенин + Рут + iOS | 500🌟", callback_data="zenin_rut")],
        [InlineKeyboardButton(text="🧠 Зенин | 200🌟", callback_data="zenin")],
        [InlineKeyboardButton(text="🔓 Нон-Рут | 15🌟", callback_data="non_root")],
        [InlineKeyboardButton(text="🎁 Кламси | FREE", callback_data="klamsi")],
        [InlineKeyboardButton(text="🛡 Рут права | 50🌟", callback_data="root")],
        [InlineKeyboardButton(text="🚫 Анти-бан | 50🌟", callback_data="antiban")],
        [InlineKeyboardButton(text="📝 Промт | 25🌟", callback_data="promt")],
        # Читы
        [InlineKeyboardButton(text="🟢 Astraldlc FREE", callback_data="free")],
        [InlineKeyboardButton(text="💎 Astraldlc PREMIUM", callback_data="premium")],
        [InlineKeyboardButton(text="⏳ В разработке", callback_data="dev")],
        # Навигация
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад в магазин", callback_data="shop"),
         InlineKeyboardButton(text="✍️ Админ", url=ADMIN_URL)]
    ])

# --- ОБРАБОТЧИКИ ---
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(START_TEXT, reply_markup=main_menu_kb())

@router.callback_query(F.data == "shop")
async def cb_shop(call: CallbackQuery):
    await call.message.edit_text(SHOP_TEXT, reply_markup=shop_kb())
    await call.answer()

@router.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery):
    await call.message.edit_text(SUPPORT_TEXT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "back")
async def cb_back(call: CallbackQuery):
    await call.message.edit_text(START_TEXT, reply_markup=main_menu_kb())
    await call.answer()

# Обработка товаров
@router.callback_query(F.data == "priv")
async def cb_priv(call: CallbackQuery):
    await call.message.edit_text(TEXT_PRIVAT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "zenin_rut")
async def cb_zenin_rut(call: CallbackQuery):
    await call.message.edit_text(TEXT_ZENIN_RUT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "zenin")
async def cb_zenin(call: CallbackQuery):
    await call.message.edit_text(TEXT_ZENIN, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "non_root")
async def cb_non_root(call: CallbackQuery):
    await call.message.edit_text(TEXT_NON_RUT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "klamsi")
async def cb_klamsi(call: CallbackQuery):
    await call.message.edit_text(TEXT_KLAMSI, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "root")
async def cb_root(call: CallbackQuery):
    await call.message.edit_text(TEXT_ROOT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "antiban")
async def cb_antiban(call: CallbackQuery):
    await call.message.edit_text(TEXT_ANTIBAN, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "promt")
async def cb_promt(call: CallbackQuery):
    await call.message.edit_text(TEXT_PROMPT, reply_markup=back_kb())
    await call.answer()

# Обработка читов
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
