import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

SELECT_PIZZA, SELECT_SIZE, SELECT_DRINK, CONFIRM_ORDER = range(4)

PIZZAS = {
    "1": {"name": "Маргарита", "price": 350},
    "2": {"name": "Пепперони", "price": 450},
    "3": {"name": "Гавайская", "price": 400},
    "4": {"name": "Четыре сыра", "price": 480},
}

SIZES = {
    "S": {"name": "Маленькая", "multiplier": 1.0},
    "M": {"name": "Средняя", "multiplier": 1.3},
    "L": {"name": "Большая", "multiplier": 1.6},
}

DRINKS = {
    "1": {"name": "Кола", "price": 100},
    "2": {"name": "Фанта", "price": 100},
    "3": {"name": "Сок", "price": 120},
    "4": {"name": "Вода", "price": 80},
    "5": {"name": "Без напитка", "price": 0},
}

TOKEN = "token"


async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()

    keyboard = [
        ["1. Маргарита (350₽)", "2. Пепперони (450₽)"],
        ["3. Гавайская (400₽)", "4. Четыре сыра (480₽)"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🍕 Добро пожаловать в пиццерию!\n\n"
        "Выберите вид пиццы:",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )

    return SELECT_PIZZA


async def select_pizza(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()

    if not text:
        await update.message.reply_text("Пожалуйста, выберите пиццу из списка.")
        return SELECT_PIZZA

    choice = text[0]

    if choice not in PIZZAS:
        await update.message.reply_text("Пожалуйста, выберите пиццу из списка.")
        return SELECT_PIZZA

    context.user_data["pizza"] = PIZZAS[choice]

    keyboard = [["S - Маленькая", "M - Средняя", "L - Большая"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"Выбрана пицца: {PIZZAS[choice]['name']}\n\n"
        "Теперь выберите размер:",
        reply_markup=reply_markup,
    )

    return SELECT_SIZE


async def select_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip().upper()

    if not text:
        await update.message.reply_text("Пожалуйста, выберите размер из списка.")
        return SELECT_SIZE

    choice = text[0]

    if choice not in SIZES:
        await update.message.reply_text("Пожалуйста, выберите размер из списка.")
        return SELECT_SIZE

    context.user_data["size"] = SIZES[choice]

    keyboard = [
        ["1. Кола (100₽)", "2. Фанта (100₽)"],
        ["3. Сок (120₽)", "4. Вода (80₽)"],
        ["5. Без напитка"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"Размер: {SIZES[choice]['name']}\n\n"
        "Выберите напиток:",
        reply_markup=reply_markup,
    )

    return SELECT_DRINK


async def select_drink(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()

    if not text:
        await update.message.reply_text("Пожалуйста, выберите напиток из списка.")
        return SELECT_DRINK

    choice = text[0]

    if choice not in DRINKS:
        await update.message.reply_text("Пожалуйста, выберите напиток из списка.")
        return SELECT_DRINK

    context.user_data["drink"] = DRINKS[choice]

    pizza_price = context.user_data["pizza"]["price"]
    size_multiplier = context.user_data["size"]["multiplier"]
    drink_price = context.user_data["drink"]["price"]

    total_price = pizza_price * size_multiplier + drink_price
    context.user_data["total"] = total_price

    keyboard = [["✅ Подтвердить заказ", "❌ Отменить заказ"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "📋 Ваш заказ:\n\n"
        f"🍕 Пицца: {context.user_data['pizza']['name']}\n"
        f"📏 Размер: {context.user_data['size']['name']}\n"
        f"🥤 Напиток: {context.user_data['drink']['name']}\n\n"
        f"💰 Итого: {total_price:.0f}₽\n\n"
        "Подтверждаете заказ?",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )

    return CONFIRM_ORDER


async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text

    if "Подтвердить" in choice:
        total = context.user_data.get("total", 0)

        await update.message.reply_text(
            "✅ Заказ подтвержден!\n\n"
            "Спасибо за заказ! Ожидайте доставку.\n"
            f"Сумма к оплате: {total:.0f}₽\n\n"
            "Для нового заказа введите /start",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="Markdown",
        )
        return ConversationHandler.END

    elif "Отменить" in choice:
        await update.message.reply_text(
            "❌ Заказ отменен.\n\n"
            "Для нового заказа введите /start",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    else:
        keyboard = [["✅ Подтвердить заказ", "❌ Отменить заказ"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(
            "Пожалуйста, выберите 'Подтвердить заказ' или 'Отменить заказ'",
            reply_markup=reply_markup,
        )

        return CONFIRM_ORDER


async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Заказ отменен. Для нового заказа введите /start",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def help_command_pizza(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    help_text = """
🍕 Бот пиццерии - справка

Доступные команды:
/start - Начать новый заказ
/cancel - Отменить текущий заказ
/help - Показать эту справку

Процесс заказа:
1. Выберите вид пиццы
2. Выберите размер
3. Выберите напиток
4. Подтвердите заказ
"""
    await update.message.reply_text(help_text)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    order_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_order)],
        states={
            SELECT_PIZZA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, select_pizza)
            ],
            SELECT_SIZE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, select_size)
            ],
            SELECT_DRINK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, select_drink)
            ],
            CONFIRM_ORDER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_order)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_order)],
    )

    application.add_handler(order_handler)
    application.add_handler(CommandHandler("help", help_command_pizza))

    print("Бот пиццерии запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
