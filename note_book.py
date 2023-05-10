import telebot
from telebot import types
from datetime import time, date, datetime, timedelta
from ntcn import time

bot = telebot.TeleBot('5952076543:AAEMZWFAHsVQGXs7bwj__nBcUqNYw5EVnug')

a = {}


#Главное меню
markup = types.InlineKeyboardMarkup(row_width=1)
item = types.InlineKeyboardButton('Показать список.', callback_data='id_list')
item2 = types.InlineKeyboardButton('Ввести новую заметку.', callback_data='id_new')
item4 = types.InlineKeyboardButton('Удалить заметку.', callback_data='id_del')
markup.add(item, item2, item4)


#Вернутся в меню
markup1 = types.InlineKeyboardMarkup(row_width=1)
item3 = types.InlineKeyboardButton('Вернутся назад.', callback_data='id_back')
markup1.add(item3)


#Удалить заметку
def delete2(message):
    try:
        if int(message.text) not in a.keys():
            bot.send_message(message.chat.id, 'Нет такой заметки.', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Заметка удалена.', reply_markup=markup)
            a.pop(int(message.text))
    except ValueError:
        bot.send_message(message.chat.id, 'Неверное значение.',reply_markup=markup)


#Добавить заметку
def msg2(message):
        bot.send_message(message.chat.id, 'Заметка добавлена.', reply_markup=markup)
        if len(a) == 0:
            a[1] = message.text
        else:
            a[max(list(a.keys()))+1] = message.text


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Выберите пункт меню.', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == 'id_list':
            if len(a) == 0:
                bot.send_message(call.message.chat.id, 'Список пуст.')
            for i in range(len(a)):
                bot.send_message(call.message.chat.id, f'{list(a.keys())[i]} - {list(a.values())[i]}')
            bot.send_message(call.message.chat.id, 'Вернуться в меню.', reply_markup=markup1)
        elif call.data == 'id_back':
            bot.send_message(call.message.chat.id, start(call.message))
        elif call.data == 'id_new':
            msg = (bot.send_message(call.message.chat.id, 'Введите сообщение.'))
            bot.register_next_step_handler(msg, msg2)
        elif call.data == 'id_del':
            msg = bot.send_message(call.message.chat.id, 'Выберите номер заметки.')
            bot.register_next_step_handler(msg, delete2)


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, 'Используйте меню.', reply_markup=markup)


bot.polling(non_stop = True, interval=0)
