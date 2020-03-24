# -*- coding: utf-8 -*-
import telebot


keyboard_main = telebot.types.InlineKeyboardMarkup()
keyboard_main.add(telebot.types.InlineKeyboardButton(text='Погода', callback_data='weather'))
keyboard_main.add(telebot.types.InlineKeyboardButton(text='Менеджер паролей', callback_data='manager_password'))

keyboard_geo = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
keyboard_geo.add(telebot.types.KeyboardButton('Поделиться геолокацией', request_location=True))

keyboard_manager_password = telebot.types.InlineKeyboardMarkup()
keyboard_manager_password.add(telebot.types.InlineKeyboardButton(text='Показать сохраненные логины/пароли', callback_data='show'))
keyboard_manager_password.add(telebot.types.InlineKeyboardButton(text='Добавить новый логин/пароль', callback_data='add'))
keyboard_manager_password.add(telebot.types.InlineKeyboardButton(text='Удалить логин/пароль', callback_data='remove'))

keyboard_manager_password_show = telebot.types.InlineKeyboardMarkup()
keyboard_manager_password_show.add(telebot.types.InlineKeyboardButton(text='Показать все', callback_data='show_all'))
keyboard_manager_password_show.add(telebot.types.InlineKeyboardButton(text='Показать конкретную', callback_data='show_one'))

keyboard_right_wrong = telebot.types.InlineKeyboardMarkup()
keyboard_right_wrong.add(telebot.types.InlineKeyboardButton(text='Верно', callback_data='right'))
keyboard_right_wrong.add(telebot.types.InlineKeyboardButton(text='Неверно', callback_data='wrong'))

keyboard_remove_right_wrong = telebot.types.InlineKeyboardMarkup()
keyboard_remove_right_wrong.add(telebot.types.InlineKeyboardButton(text='Да', callback_data='remove_right'))
keyboard_remove_right_wrong.add(telebot.types.InlineKeyboardButton(text='Нет', callback_data='remove_wrong'))
