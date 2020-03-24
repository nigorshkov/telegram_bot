# -*- coding: utf-8 -*-
import telebot
from lib import weather, keyboard, config, information, database

bot = telebot.TeleBot(config.token)
info_dict = {}
db_worked = database.SQL(config.database_name)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, {}'.format(message.chat.first_name.encode('UTF-8')),
                     reply_markup = keyboard.keyboard_main)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'weather':
        msg = bot.send_message(call.message.chat.id, 'Отправьте свою геолокацию',
                               reply_markup = keyboard.keyboard_geo)
        bot.register_next_step_handler(msg, wethear)
    elif call.data == 'manager_password':
        if db_worked.check_create_user(call.message.chat.id) == 0:
            db_worked.insert_user(call.message.chat.id, call.message.chat.username, call.message.chat.first_name,
                                  call.message.chat.last_name)
        bot.send_message(call.message.chat.id, 'Что Вы хотите сделать?',
                         reply_markup = keyboard.keyboard_manager_password)
    elif call.data == 'show':
        if db_worked.count_rows(call.message.chat.id) != 0:
            bot.send_message(call.message.chat.id, 'Показать все записи или конкретную?',
                             reply_markup = keyboard.keyboard_manager_password_show)
        else:
            bot.send_message(call.message.chat.id, 'Вы не добавляли логины/пароли',
                             reply_markup = keyboard.keyboard_main)
    elif call.data == 'show_all':
        bot.send_message(call.message.chat.id, db_worked.show_all(call.message.chat.id),
                         reply_markup = keyboard.keyboard_main)
    elif call.data == 'show_one':
        msg = bot.send_message(call.message.chat.id, 'Введите название сайта')
        bot.register_next_step_handler(msg, find_one_logpass)
    elif call.data == 'add':
        msg = bot.send_message(call.message.chat.id, 'Введите уникальное название сайта:')
        bot.register_next_step_handler(msg, process_name_step)
    elif call.data == 'remove':
        msg = bot.send_message(call.message.chat.id, 'Введите название сайта:')
        bot.register_next_step_handler(msg, remove)
    elif call.data == 'right':
        db_worked.insert(call.message.chat.id, info_dict[call.message.chat.id].name,
                         info_dict[call.message.chat.id].login, info_dict[call.message.chat.id].password)
        bot.send_message(call.message.chat.id, 'Данные сохранены!', reply_markup = keyboard.keyboard_main)
    elif call.data == 'wrong':
        bot.send_message(call.message.chat.id, 'Данные не добавлены', reply_markup = keyboard.keyboard_main)
    elif call.data == 'remove_right':
        db_worked.commit()
        bot.send_message(call.message.chat.id, 'Данные удалены!', reply_markup = keyboard.keyboard_main)
    elif call.data == 'remove_wrong':
        db_worked.rollback()
        bot.send_message(call.message.chat.id, 'Данные неудалены!', reply_markup = keyboard.keyboard_main)


@bot.message_handler(content_types=['text'])
def message(message):
    bot.send_message(message.chat.id, 'Команда не определена', reply_markup = keyboard.keyboard_main)

def wethear(message):
    try:
        bot.send_message(message.chat.id, weather.get_weater(message.location.latitude,
                                                             message.location.longitude),
                         parse_mode="Markdown", reply_markup = keyboard.keyboard_main)
    except:
        bot.reply_to(message, 'Нужно поделиться геолокацией!', reply_markup = keyboard.keyboard_main)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        info = information.Info(name)
        info_dict[chat_id] = info
        if db_worked.show_one(chat_id, name) == '':
            msg = bot.send_message(message.chat.id, 'Введите логин:')
            bot.register_next_step_handler(msg, process_login_step)
        else:
            bot.send_message(message.chat.id, 'Сайт с таким названием уже добавлен!',
                             reply_markup = keyboard.keyboard_main)
    except Exception as e:
        bot.reply_to(message, 'Что то пошло не так(')


def process_login_step(message):
    try:
        login = message.text
        info = info_dict[message.chat.id]
        info.login = login
        msg = bot.send_message(message.chat.id, 'Введите пароль:')
        bot.register_next_step_handler(msg, process_password_step)
    except Exception as e:
        bot.reply_to(message, 'Что то пошло не так(')


def process_password_step(message):
    try:
        password = message.text
        info = info_dict[message.chat.id]
        info.password = password
        bot.send_message(message.chat.id,
                         'Название: {}\nЛогин: {}\nПароль: {}'.format(info.name.encode('UTF-8'),
                                                                      info.login.encode('UTF-8'),
                                                                      info.password.encode('UTF-8')))
        bot.send_message(message.chat.id, 'Верны ли введеные данные?',
                         reply_markup = keyboard.keyboard_right_wrong)
    except Exception as e:
        bot.reply_to(message, 'Что то пошло не так(')

def find_one_logpass(message):
    try:
        name = message.text
        if db_worked.show_one(message.chat.id, name) != '':
            bot.send_message(message.chat.id, db_worked.show_one(message.chat.id, name),
                             reply_markup = keyboard.keyboard_main)
        else:
            bot.send_message(message.chat.id, 'Логин/пароль не найден', reply_markup = keyboard.keyboard_main)
    except Exception as e:
        bot.reply_to(message, 'Что то пошло не так(')

def remove(message):
    try:
        name = message.text
        if db_worked.show_one(message.chat.id, name) != '':
            bot.send_message(message.chat.id, db_worked.show_one(message.chat.id, name))
            db_worked.remove(message.chat.id, name)
            bot.send_message(message.chat.id, 'Вы хотите удалить следующий логин/пароль?',
                             reply_markup = keyboard.keyboard_remove_right_wrong)
        else:
            bot.send_message(message.chat.id, 'Логин пароль не найден', reply_markup = keyboard.keyboard_main)
    except Exception as e:
        bot.reply_to(message, 'Что то пошло не так(')

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(none_stop=True)
