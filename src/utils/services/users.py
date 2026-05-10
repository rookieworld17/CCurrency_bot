from telebot import types
from utils.services.welcome import get_welcome_message
from utils.services.database import add_user, get_language, set_language
from utils.translations import STRINGS
import os

channel_username = os.getenv('CHANNEL_USERNAME')
channel_invite_lnk = os.getenv('CHANNEL_INVITE_LINK') or f"https://t.me/{channel_username.lstrip('@')}"

def get_subscription_keyboard(lang: str = 'EN') -> types.InlineKeyboardMarkup:
    s = STRINGS[lang]
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            s['subscribe_btn'],
            url=f"{channel_invite_lnk}"
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            s['check_sub_btn'],
            callback_data="check_sub"
        )
    )
    return markup

def get_language_keyboard(lang: str) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            STRINGS[lang]['lang_btn'],
            callback_data='toggle_lang'
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
        lang = get_language(call.from_user.id)
        if check_subscribe(bot, call.from_user.id):
            bot.send_message(
                call.message.chat.id,
                get_welcome_message(lang),
                parse_mode="MarkdownV2",
                reply_markup=get_language_keyboard(lang),
                link_preview_options=types.LinkPreviewOptions(is_disabled=True)
            )
        else:
            bot.send_message(
                call.message.chat.id,
                STRINGS[lang]['not_subscribed'],
                reply_markup=get_subscription_keyboard(lang),
                parse_mode="MarkdownV2"
            )

    @bot.callback_query_handler(func=lambda call: call.data == "toggle_lang")
    def callback_toggle_language(call):
        user_id = call.from_user.id
        add_user(user_id, call.from_user.username)
        current_lang = get_language(user_id)
        new_lang = 'RU' if current_lang == 'EN' else 'EN'
        set_language(user_id, new_lang)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_welcome_message(new_lang),
            parse_mode='MarkdownV2',
            reply_markup=get_language_keyboard(new_lang),
            link_preview_options=types.LinkPreviewOptions(is_disabled=True)
        )
        bot.answer_callback_query(call.id)
