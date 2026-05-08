from dotenv import load_dotenv
from telebot import types
from utils.services.welcome import get_welcome_message
from utils.services.formatting import parce_input
from utils.token import convert_currency, get_token_info
from utils.services.database import init_db, add_user, get_language
from utils.services.users import check_subscribe, get_subscription_keyboard, get_language_keyboard
from utils.services import users
from utils.translations import STRINGS
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

    lang = get_language(message.from_user.id)

    if not check_subscribe(bot, message.from_user.id):
        bot.reply_to(
            message,
            STRINGS[lang]['subscribe_required'],
            reply_markup=get_subscription_keyboard(lang),
            parse_mode="MarkdownV2",
        )
        return

    add_user(message.from_user.id)

    bot.send_message(
        message.chat.id,
        get_welcome_message(lang),
        parse_mode="MarkdownV2",
        reply_markup=get_language_keyboard(lang),
        link_preview_options=types.LinkPreviewOptions(is_disabled=True)
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if is_spam(message.from_user.id):
        return

    lang = get_language(message.from_user.id)

    if not check_subscribe(bot, message.from_user.id):
        bot.reply_to(
            message,
            STRINGS[lang]['subscribe_required'],
            reply_markup=get_subscription_keyboard(lang),
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
                convert_currency(amount, symbol, intent=intent, lang=lang),
                parse_mode='MarkdownV2',
                link_preview_options=types.LinkPreviewOptions(is_disabled=True)
            )
        except Exception:
            bot.reply_to(message, STRINGS[lang]['forward_error'], parse_mode='MarkdownV2')
        return

    if intent == 'reverse':
        try:
            bot.reply_to(
                message,
                convert_currency(amount, symbol, intent=intent, lang=lang),
                parse_mode='MarkdownV2',
                link_preview_options=types.LinkPreviewOptions(is_disabled=True)
            )
        except Exception:
            bot.reply_to(message, STRINGS[lang]['reverse_error'], parse_mode='MarkdownV2')
        return

    if intent == 'info':
        if not symbol.isalpha() or len(symbol) > 10:
            bot.reply_to(message, STRINGS[lang]['invalid_ticker'], parse_mode='MarkdownV2')
            return
        try:
            bot.reply_to(
                message,
                get_token_info(symbol, lang=lang),
                parse_mode='MarkdownV2',
                link_preview_options=types.LinkPreviewOptions(is_disabled=True)
            )
        except Exception:
            bot.reply_to(message, STRINGS[lang]['token_not_found'], parse_mode='MarkdownV2')

    if intent == 'reverse_invalid':
        bot.reply_to(message, STRINGS[lang]['invalid_format'], parse_mode='MarkdownV2')
        return

bot.polling()
