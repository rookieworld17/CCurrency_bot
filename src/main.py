from dotenv import load_dotenv
from telebot import types
from utils.services.welcome import get_welcome_message
from utils.services.formatting import parce_input, escape_md
from utils.token import convert_currency, get_token_info
from utils.services.database import init_db, add_user
from utils.services.users import check_subscribe, get_subscription_keyboard
from utils.services import users
import os, telebot, time

load_dotenv()
init_db()

telegram_api = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(telegram_api)

users.register_callback_handlers(bot)

last_action_time = {}
ANTI_SPAM_DELAY = 5

def is_spam(user_id):
    now = time.time()
    if user_id in last_action_time and now - last_action_time[user_id] < ANTI_SPAM_DELAY:
        return True
    last_action_time[user_id] = now
    return False

@bot.message_handler(commands=["start"])
def send_welcome(message):
    if is_spam(message.from_user.id):
        return

    if not check_subscribe(bot, message.from_user.id):
        bot.reply_to(
            message,
            "*Для того чтобы пользоваться функционалом бота, необходимо подписаться на канал* 😉",
            reply_markup=get_subscription_keyboard(),
            parse_mode="MarkdownV2",
        )
        return

    add_user(message.from_user.id)

    bot.send_message(
        message.chat.id,
        get_welcome_message(),
        parse_mode="MarkdownV2",
        link_preview_options=types.LinkPreviewOptions(
            is_disabled=True
        )
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if is_spam(message.from_user.id):
        return

    if not check_subscribe(bot, message.from_user.id):
        bot.reply_to(
            message,
             "*Для того чтобы пользоваться функционалом бота, необходимо подписаться на канал* 😉",
            reply_markup=get_subscription_keyboard(),
            parse_mode="MarkdownV2",
        )
        return

    add_user(message.from_user.id)

    text = message.text.strip()
    amount, symbol, intent = parce_input(text)

    if intent == 'forward':
        try:
            bot.reply_to(
                message,
                convert_currency(
                    amount,
                    symbol,
                    intent=intent
                ),
                parse_mode='MarkdownV2',
                link_preview_options=types.LinkPreviewOptions(
                    is_disabled=True
                )
            )
        except Exception:
            bot.reply_to(message, escape_md("⚠️ *Не удалось конвертировать сумму*. Проверьте правильность ввода."), parse_mode='MarkdownV2')
        return

    if intent == 'reverse':
        try:
            bot.reply_to(
                message,
                convert_currency(
                    amount,
                    symbol,
                    intent=intent
                ),
                parse_mode='MarkdownV2',
                link_preview_options=types.LinkPreviewOptions(
                    is_disabled=True
                )
            )
        except Exception:
            bot.reply_to(message, escape_md("⚠️ *Ошибка при обратной конвертации*. Проверьте правильность ввода."), parse_mode='MarkdownV2')
        return

    if intent == 'info':
        if not symbol.isalpha() or len(symbol) > 10:
            bot.reply_to(message, escape_md("❌ *Невозможно обработать запрос*. Пример: `BTC`, `0.01 ETH`, `100 - BTC`"),
                         parse_mode='MarkdownV2')
            return
        try:
            bot.reply_to(
                message,
                get_token_info(symbol),
                parse_mode='MarkdownV2',
                link_preview_options = types.LinkPreviewOptions(
                    is_disabled=True
                )
            )
        except Exception:
            bot.reply_to(message, escape_md("⚠️ *Токен не найден*. Убедитесь, что тикер указан правильно."), parse_mode='MarkdownV2')

    if intent == 'reverse_invalid':
        bot.reply_to(message, escape_md("❌ *Неверный формат запроса*."), parse_mode='MarkdownV2')
        return

bot.polling()