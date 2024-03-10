from telegram import ReplyKeyboardMarkup, Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, \
    CallbackContext
from Wallet import Wallet

BOT_TOKEN = "TOKEN"
OPERATION, DECISION, GET_CASH, PLUS_CASH, MINUS_CASH = range(5)

user = Wallet(0.0)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [[]]
    await update.message.reply_text(
        'Сколько денег?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return GET_CASH


async def get_cash(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user.cash = float(update.message.text)
    reply_keyboard = [['ок']]
    await update.message.reply_text(
        'Двигаемся дальше',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return OPERATION


async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == 'стоп':
        await update.message.reply_text('Отрубаюсь')
        return ConversationHandler.END
    await update.message.reply_text(f'У тебя {user.cash} денег')
    reply_keyboard = [['Получил', 'Потратил']]
    await update.message.reply_text(
        'Жду следующую операцию',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return DECISION


async def moves(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == 'Получил':
        await update.message.reply_text('Сколько?')
        return PLUS_CASH
    elif update.message.text == 'Потратил':
        await update.message.reply_text('Сколько?')
        return MINUS_CASH
    else:
        await update.message.reply_text('Возвращаюсь обратно')
        return OPERATION


async def plus_cash(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user.cash += float(update.message.text)
    reply_keyboard = [['ок']]
    await update.message.reply_text(
        'Двигаемся дальше',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return OPERATION


async def minus_cash(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user.cash -= float(update.message.text)
    reply_keyboard = [['ок']]
    await update.message.reply_text(
        'Двигаемся дальше',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return OPERATION


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            OPERATION: [MessageHandler(filters.TEXT, reply_to_message)],
            DECISION: [MessageHandler(filters.TEXT, moves)],
            GET_CASH: [MessageHandler(filters.TEXT, get_cash)],
            PLUS_CASH: [MessageHandler(filters.TEXT, plus_cash)],
            MINUS_CASH: [MessageHandler(filters.TEXT, minus_cash)]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    app.add_handler(conversation_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
