from dotenv import load_dotenv
from telebot import types
from utils.services.welcome import get_welcome_message
from utils.services.formatting import parce_input, escape_md
from utils.token import convert_currency, get_token_info
import os, telebot, re

load_dotenv()

telegram_api = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(telegram_api)

@bot.message_handler(commands=["start"])
def send_welcome(message):
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