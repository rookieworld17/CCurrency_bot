from telebot import types
from utils.services.welcome import get_welcome_message
import os

channel_username = os.getenv('CHANNEL_USERNAME')

def get_subscription_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "📢 Подписаться на канал",
            url=f"https://t.me/{channel_username.lstrip('@')}"
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            "✅ Проверить подписку",
            callback_data="check_sub"
        )
    )
    return markup

def check_subscribe(bot, user_id) -> bool:
    try:
        member = bot.get_chat_member(channel_username, user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

def register_callback_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "check_sub")
    def callback_check_subscription(call):
        if check_subscribe(bot, call.from_user.id):
            bot.send_message(
                call.message.chat.id,
                get_welcome_message(),
                parse_mode="MarkdownV2",
                link_preview_options=types.LinkPreviewOptions(
                    is_disabled=True
                )
            )
        else:
            bot.send_message(
                call.message.chat.id,
                "*Похоже ты не подписался, попробуй еще раз* 😉",
                reply_markup=get_subscription_keyboard(),
                parse_mode="MarkdownV2"
            )