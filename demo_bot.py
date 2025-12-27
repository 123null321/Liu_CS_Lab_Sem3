import logging
from datetime import datetime
import random

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


TOKEN = "token"


# ---------- 命令 /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("📅 Дата и время"), KeyboardButton("ℹ️ Информация")],
        [KeyboardButton("🎲 Случайное число"), KeyboardButton("👤 О пользователе")],
        [KeyboardButton("🌤 Погода")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Привет! Я демонстрационный бот с кнопками.\n"
        "Выберите действие на клавиатуре ниже:",
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
📋 Доступные команды и функции:

/start - Запустить бота и показать клавиатуру
/help - Показать это сообщение
/inline - Показать inline-кнопки

Кнопки на клавиатуре:
📅 Дата и время - Показать текущую дату и время
ℹ️ Информация - Информация о боте
🎲 Случайное число - Сгенерировать случайное число
👤 О пользователе - Информация о вас
🌤 Погода - Получить информацию о погоде
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")


# 底部按钮发来的文字
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    user_message = update.message.text

    if user_message == "📅 Дата и время":
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        await update.message.reply_text(
            f"📅 Текущая дата и время:\n{now}",
            parse_mode="Markdown",
        )

    elif user_message == "ℹ️ Информация":
        info_text = """
🤖 Информация о боте:

*Название:* DemoBot
*Версия:* 1.0
*Описание:* Демонстрационный бот для лабораторной работы №5
*Функции:* Работа с кнопками, обработка команд, inline-кнопки

Разработано с использованием библиотеки python-telegram-bot
"""
        await update.message.reply_text(info_text, parse_mode="Markdown")

    elif user_message == "🎲 Случайное число":
        number = random.randint(1, 100)
        await update.message.reply_text(
            f"🎲 Ваше случайное число: {number}",
            parse_mode="Markdown",
        )

    elif user_message == "👤 О пользователе":
        user = update.message.from_user
        user_info = f"""
👤 Информация о пользователе:

*Имя:* {user.first_name}
*Фамилия:* {user.last_name or 'Не указана'}
*Username:* @{user.username or 'Не указан'}
*ID:* {user.id}
"""
        await update.message.reply_text(user_info, parse_mode="Markdown")

    elif user_message == "🌤 Погода":
        
        keyboard = [
            [
                InlineKeyboardButton("Москва", callback_data="weather_moscow"),
                InlineKeyboardButton("Санкт-Петербург", callback_data="weather_spb"),
            ],
            [
                InlineKeyboardButton("Новосибирск", callback_data="weather_nsk"),
                InlineKeyboardButton("Екатеринбург", callback_data="weather_ekb"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Выберите город для просмотра погоды:",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text(
            "Я не понимаю эту команду. Используйте кнопки на клавиатуре или /help"
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    weather_data = {
        "weather_moscow": {
            "city": "Москва",
            "temp": "+15°C",
            "condition": "☁️ Облачно",
        },
        "weather_spb": {
            "city": "Санкт-Петербург",
            "temp": "+12°C",
            "condition": "🌧 Дождь",
        },
        "weather_nsk": {
            "city": "Новосибирск",
            "temp": "+8°C",
            "condition": "⛅️ Переменная облачность",
        },
        "weather_ekb": {
            "city": "Екатеринбург",
            "temp": "+10°C",
            "condition": "☀️ Солнечно",
        },
    }

    if query.data in weather_data:
        data = weather_data[query.data]
        await query.edit_message_text(
            f"🌤 Погода в {data['city']}:\n"
            f"Температура: {data['temp']}\n"
            f"Состояние: {data['condition']}",
            parse_mode="Markdown",
        )
    else:
        await query.edit_message_text("Данные не найдены")


async def inline_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("✅ Подтвердить", callback_data="confirm"),
            InlineKeyboardButton("❌ Отмена", callback_data="cancel"),
        ],
        [
            InlineKeyboardButton(
                "🔗 Ссылка на GitHub",
                url="https://github.com/python-telegram-bot",
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Пример inline-кнопок:",
        reply_markup=reply_markup,
    )


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("inline", inline_command))

    application.add_handler(CallbackQueryHandler(button_callback))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("DemoBot запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
