from dotenv import load_dotenv
from telebot import types
from utils.services.welcome import get_welcome_message
from utils.services.formatting import parce_input
from utils.token import convert_currency, get_token_info
from utils.services.database import init_db, add_user, get_language
from utils.services.users import check_subscribe, get_subscription_keyboard, get_language_keyboard
from utils.services import users, suggestions
from utils.translations import STRINGS
import os, telebot, time, threading, math

load_dotenv()
init_db()

telegram_api = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(telegram_api)

users.register_callback_handlers(bot)

last_action_time = {}
cooldown_messages = {}
ANTI_SPAM_DELAY = int(os.getenv('ANTI_SPAM_DELAY', 5))
SUGGESTIONS_CHANNEL_ID = int(os.getenv('SUGGESTIONS_CHANNEL_ID', -1003947415284))


def get_cooldown(user_id):
    last = last_action_time.get(user_id)
    if last is None:
        return 0
    remaining = ANTI_SPAM_DELAY - (time.time() - last)
    return remaining if remaining > 0 else 0


def record_action(user_id):
    last_action_time[user_id] = time.time()


def send_cooldown_message(message, lang, remaining):
    user_id = message.from_user.id

    if user_id in cooldown_messages:
        existing = cooldown_messages[user_id]
        existing['stop'].set()
        try:
            bot.delete_message(existing['msg'].chat.id, existing['msg'].message_id)
        except Exception:
            pass

    secs = math.ceil(remaining)
    sent = bot.reply_to(message, STRINGS[lang]['cooldown_wait'].format(secs=secs))
    stop_event = threading.Event()
    cooldown_messages[user_id] = {'msg': sent, 'stop': stop_event}

    def countdown():
        for s in range(secs - 1, 0, -1):
            if stop_event.wait(1):
                return
            try:
                bot.edit_message_text(
                    STRINGS[lang]['cooldown_wait'].format(secs=s),
                    sent.chat.id, sent.message_id
                )
            except Exception:
                pass
        if stop_event.wait(1):
            return
        try:
            bot.edit_message_text(STRINGS[lang]['cooldown_done'], sent.chat.id, sent.message_id)
        except Exception:
            pass
        if cooldown_messages.get(user_id, {}).get('stop') is stop_event:
            cooldown_messages.pop(user_id, None)

    threading.Thread(target=countdown, daemon=True).start()


@bot.message_handler(commands=["start"])
def send_welcome(message):
    lang = get_language(message.from_user.id)

    if not check_subscribe(bot, message.from_user.id):
        bot.reply_to(
            message,
            STRINGS[lang]['subscribe_required'],
            reply_markup=get_subscription_keyboard(lang),
            parse_mode="MarkdownV2",
        )
        return

    add_user(message.from_user.id, message.from_user.username)

    bot.send_message(
        message.chat.id,
        get_welcome_message(lang),
        parse_mode="MarkdownV2",
        reply_markup=get_language_keyboard(lang),
        link_preview_options=types.LinkPreviewOptions(is_disabled=True)
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    lang = get_language(message.from_user.id)

    if not check_subscribe(bot, message.from_user.id):
        bot.reply_to(
            message,
            STRINGS[lang]['subscribe_required'],
            reply_markup=get_subscription_keyboard(lang),
            parse_mode="MarkdownV2",
        )
        return

    add_user(message.from_user.id, message.from_user.username)

    if suggestions.is_pending(message.from_user.id):
        suggestions.clear_pending(message.from_user.id)
        suggestions.record_submission(message.from_user.id)
        identifier = f"@{message.from_user.username}" if message.from_user.username else str(message.from_user.id)
        try:
            bot.send_message(SUGGESTIONS_CHANNEL_ID, f"{identifier}\n\n{message.text}")
        except Exception:
            pass
        bot.reply_to(message, STRINGS[lang]['suggest_thanks'], parse_mode='MarkdownV2')
        return

    text = message.text.strip()
    amount, symbol, intent = parce_input(text)

    if intent == 'reverse_invalid':
        bot.reply_to(message, STRINGS[lang]['invalid_format'], parse_mode='MarkdownV2')
        return

    if intent == 'info' and (not symbol.isalpha() or len(symbol) > 10):
        bot.reply_to(message, STRINGS[lang]['invalid_ticker'], parse_mode='MarkdownV2')
        return

    remaining = get_cooldown(message.from_user.id)
    if remaining > 0:
        send_cooldown_message(message, lang, remaining)
        return
    record_action(message.from_user.id)

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
        try:
            bot.reply_to(
                message,
                get_token_info(symbol, lang=lang),
                parse_mode='MarkdownV2',
                link_preview_options=types.LinkPreviewOptions(is_disabled=True)
            )
        except Exception:
            bot.reply_to(message, STRINGS[lang]['token_not_found'], parse_mode='MarkdownV2')

@bot.message_handler(
    content_types=['photo', 'video', 'audio', 'document', 'voice', 'sticker', 'animation', 'contact', 'location'],
    func=lambda message: suggestions.is_pending(message.from_user.id)
)
def handle_suggestion_non_text(message):
    lang = get_language(message.from_user.id)
    suggestions.clear_pending(message.from_user.id)
    bot.reply_to(message, STRINGS[lang]['suggest_non_text'], parse_mode='MarkdownV2')


bot.polling()
