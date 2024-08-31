# step of faith telegram bot
import os

from dotenv import load_dotenv
import telebot
from telebot import types
import yaml

import google_sheets_module as sheets
import sql_functions
import user_utils
import utils


read = load_dotenv(".env")
token = os.getenv("BOT_TOKEN")

with open("replies.yaml", encoding="utf-8") as f:
    replies = yaml.safe_load(f)

bot = telebot.TeleBot(token)

logger = utils.get_logger(__name__)


# function show menu
def function_show_menu(callback: types.CallbackQuery) -> None:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn_schedule = types.InlineKeyboardButton(
        text=replies['button']['menu']['schedule'],
        callback_data='func_schedule'
    )
    btn_appointment = types.InlineKeyboardButton(
        text=replies['button']['menu']['appointment'],
        callback_data='func_appointment'
    )
    btn_question = types.InlineKeyboardButton(
        text=replies['button']['menu']['question'],
        callback_data='func_question'
    )
    btn_feedback = types.InlineKeyboardButton(
        text=replies['button']['menu']['feedback'],
        callback_data='func_feedback'
    )
    btn_social_networks = types.InlineKeyboardButton(
        text=replies['button']['menu']['social_networks'],
        callback_data='func_social_networks'
    )
    btn_church_schedule = types.InlineKeyboardButton(
        text=replies['button']['menu']['church_schedule'],
        callback_data='func_church_schedule'
    )
    cancel = types.InlineKeyboardButton(
        text=replies['button']['cancel'],
        callback_data='func_cancel'
    )
    keyboard.add(
        btn_schedule, btn_appointment,
        btn_question, btn_feedback,
        btn_social_networks, btn_church_schedule,
        cancel
    )
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=replies['button']['menu']['text'],
        reply_markup=keyboard
    )


# function for getting schedule
def function_show_schedule(callback: types.CallbackQuery) -> None:
    schedule_text = user_utils.make_schedule_text(sheets.get_schedule())
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cancel = types.InlineKeyboardButton(
        text=replies['button']['cancel'],
        callback_data='func_menu'
    )
    keyboard.add(cancel)
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=schedule_text,
        reply_markup=keyboard
    )


# function for make an appointment with a clergyman
def function_make_appointment(callback: types.CallbackQuery) -> None:
    pass


# function for write question
def function_ask_question(callback: types.CallbackQuery) -> None:
    pass


# function for write feedback
def function_write_feedback(callback: types.CallbackQuery) -> None:
    pass


# function send social network
def function_show_social_networks(callback: types.CallbackQuery) -> None:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    telegram_btn = types.InlineKeyboardButton(
        text=replies['button']['social_networks']['telegram'],
        url=replies['button']['social_networks']['telegram_url']
    )
    instagram_btn = types.InlineKeyboardButton(
        text=replies['button']['social_networks']['instagram'],
        url=replies['button']['social_networks']['instagram_url']
    )
    cancel = types.InlineKeyboardButton(
        text=replies['button']['cancel'],
        callback_data='func_menu'
    )
    keyboard.add(telegram_btn, instagram_btn, cancel)
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=replies['button']['social_networks']['text'],
        reply_markup=keyboard
    )


# function send church schedule
def function_show_church_schedule(callback: types.CallbackQuery) -> None:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cancel = types.InlineKeyboardButton(
        text=replies['button']['cancel'],
        callback_data='func_menu'
    )
    keyboard.add(cancel)
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=replies['button']['church_schedule']['text'],
        reply_markup=keyboard
    )


# echo command
@bot.message_handler(regexp="^echo ")
def echo(message: types.Message) -> None:
    bot.send_message(message.from_user.id, message.text[5:])


# command start
@bot.message_handler(commands=["start", "help", "menu"])
def menu(message: telebot.types.Message) -> None:
    if not sql_functions.check_user_id(message.from_user.id):
        sql_functions.add_to_database(message.from_user.id, message.from_user.username)
    if not sql_functions.is_banned(message.from_user.id):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        menu_btn = types.InlineKeyboardButton(
            text=replies['button']['menu']['btn_text'],
            callback_data='func_menu'
        )
        keyboard.add(menu_btn)
        bot.send_message(
            message.from_user.id,
            replies['welcome'],
            reply_markup=keyboard
        )
    else:
        bot.send_message(message.from_user.id, replies['ban']['banned'])


# check callback data
@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback: types.CallbackQuery) -> None:

    if callback.data == 'func_menu':
        function_show_menu(callback)
    elif callback.data == 'func_schedule':
        function_show_schedule(callback)
    elif callback.data == 'func_appointment':
        function_make_appointment(callback)
    elif callback.data == 'func_question':
        function_ask_question(callback)
    elif callback.data == 'func_feedback':
        function_write_feedback(callback)
    elif callback.data == 'func_social_networks':
        function_show_social_networks(callback)
    elif callback.data == 'func_church_schedule':
        function_show_church_schedule(callback)
    elif callback.data == 'func_cancel':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)


# command ban
@bot.message_handler(regexp="^/ban ")
def ban(message: types.Message) -> None:
    if not sql_functions.is_banned(message.from_user.id):
        if sql_functions.is_admin(message.from_user.id):
            username = user_utils.select_username_from_text(message.text[5:])
            completed = sql_functions.change_ban_status(username, 1)
            if completed:
                bot.send_message(
                    message.from_user.id,
                    replies['ban']['success'].format(username=username)
                )
            else:
                bot.send_message(message.from_user.id, replies['ban']['failure'])
    else:
        bot.send_message(message.from_user.id, replies['ban']['banned'])


# command ban
@bot.message_handler(regexp="^/unban ")
def unban(message: types.Message) -> None:
    if not sql_functions.is_banned(message.from_user.id):
        if sql_functions.is_admin(message.from_user.id):
            username = user_utils.select_username_from_text(message.text[7:])
            completed = sql_functions.change_ban_status(username, 0)
            if completed:
                bot.send_message(
                    message.from_user.id,
                    replies['unban']['success'].format(username=username)
                )
            else:
                bot.send_message(message.from_user.id, replies['unban']['failure'])
    else:
        bot.send_message(message.from_user.id, replies['ban']['banned'])


# RUN BOT
logger.info("START BOT...")
bot.polling()
