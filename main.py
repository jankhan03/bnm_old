
import datetime

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings import token
from create_bd import create_db
import db_functions
from telebot import types
import re

name = ''
description = ''
instagram_username = ''
telegram_username = ''
photo_id = ''

stage_of_registration = 0

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['photo'])
def photo_hendler(message):

    global photo_id

    photo_id = message.photo[-1].file_id

    if stage_of_registration == 5:

        bot.send_message(message.chat.id, '🎉 Поздравляю, вы зарегистрировались 🎉\nНам понадобится некотороые время, чтобы проверить достоверность данных. При возникновении вопросов, пишите в телегу @ceobuddy\n\nВернуться в главное меню\n/main_menu')

        add_master_to_bd_after_registration()




def add_master_to_bd_after_registration():

    global name
    global description
    global instagram_username
    global telegram_username
    global photo_id
    global stage_of_registration

    db_functions.add_master([
        name,
        description,
        instagram_username,
        telegram_username,
        photo_id
    ])

    name = ''
    description = ''
    instagram_username = ''
    telegram_username = ''
    photo_id = ''

    stage_of_registration = 0



def gen_main_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.row_height = 3
    markup.add(InlineKeyboardButton("📘 Список", callback_data="/masters"),
               InlineKeyboardButton("🎊 Регистрация", callback_data="/registration"))
    return markup


def stage_of_registration_markup():

    global stage_of_registration

    markup = InlineKeyboardMarkup()

    markup.row_width = 3

    markup.row_height = 3

    if stage_of_registration == 1:

        markup.add(InlineKeyboardButton("➡️ Продолжить регистрацию", callback_data="/registration1"))

    if stage_of_registration == 2:
        markup.add(InlineKeyboardButton("➡️ Продолжить регистрацию", callback_data="/registration2"))

    if stage_of_registration == 3:
        markup.add(InlineKeyboardButton("➡️ Продолжить регистрацию", callback_data="/registration3"))

    if stage_of_registration == 4:
        markup.add(InlineKeyboardButton("➡️ Продолжить регистрацию", callback_data="/registration4"))

    return markup

@bot.message_handler(content_types=['location'])
def location (message):
    if message.location is not None:
        print(message.location.longitude)
        print(message.location.latitude)


@bot.message_handler(commands=['start'])
def start_message(message):

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)
    bot.send_message(message.chat.id, "Привет! При помощи этого бота ты найдешь маникюрщиц и сможшеь сразу же им написать! Такжe ты можешь зарегистрироваться и попасть в этот самый список маникюрщиц.", reply_markup=gen_main_markup())


@bot.message_handler(commands=['main_menu'])
def start_message(message):
    bot.send_message(message.chat.id, 'Меню:', reply_markup=gen_main_markup())


@bot.message_handler(func=lambda message: True)
def message_handler(message):

    global name
    global description
    global instagram_username
    global telegram_username
    global photo_id

    global stage_of_registration

    if stage_of_registration == 0:

        stage_of_registration += 1

        name = message.text

        bot.send_message(message.chat.id, 'Данные получены', reply_markup=stage_of_registration_markup())

    elif stage_of_registration == 1:

        stage_of_registration += 1

        description = message.text

        bot.send_message(message.chat.id, 'Данные получены', reply_markup=stage_of_registration_markup())

    elif stage_of_registration == 2:

        stage_of_registration += 1

        instagram_username = message.text

        bot.send_message(message.chat.id, 'Данные получены', reply_markup=stage_of_registration_markup())

    elif stage_of_registration == 3:

        stage_of_registration += 1

        telegram_username = message.text

        bot.send_message(message.chat.id, 'Данные получены', reply_markup=stage_of_registration_markup())


# Обработчик нажатия на кнопки. Именно здесь заключена основная логика бота.
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global name
    global description
    global instagram_username
    global telegram_username
    global stage_of_registration

    if call.data == "/masters":

        for master in db_functions.get_masters_list():
            bot.send_photo(call.message.chat.id,
                           f'{master[4]}',
                           caption=f'{master[0]}\n\n⭐ {master[1]}\n\n⭐️ Инстаграм: https://www.instagram.com/{master[3]}\n\n⭐ Телеграм: @{master[2]}\n\nНажми, чтобы вернуться в главное меню\n\n👇👇👇👇\n/main_menu')

    elif call.data == "/registration":

        bot.send_message(call.message.chat.id, 'Введите свое имя:')

    elif call.data == "/registration1":

        bot.send_message(call.message.chat.id, 'Введи описание:')

    elif call.data == "/registration2":

        bot.send_message(call.message.chat.id, 'Введи ник в инсте:')

    elif call.data == "/registration3":

        bot.send_message(call.message.chat.id, 'Введи ник в телеге:')

    elif call.data == "/registration4":

        bot.send_message(call.message.chat.id, 'Скидывай фотку')

        stage_of_registration += 1



print('Bot in work....')
create_db()
bot.polling(none_stop=True, interval=0)
