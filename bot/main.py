from typing import Optional

import telebot
import random
import flask
import time
import logging
from telebot import types
from datetime import datetime

API_TOKEN = '6402634448:AAGq1MQC1OtiXPxW9ybdWiCLrG_pBAQaEQI'
APP_HOST = '127.0.0.1'
APP_PORT = 8444
WEB_HOOK_URL = 'https://7f42-217-107-125-211.ngrok.io'

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)

last_inc_num = 0


class Inc:
    def __init__(self, number: int, start_time: str, description: Optional[str] = None, update: Optional[str] = None,
                 update_time: Optional[str] = None, end_time: Optional[str] = None):
        self.number: int = number
        self.description: str = description
        self.update: str = update
        self.start_time: str = start_time
        self.update_time: str = update_time
        self.end_time: str = end_time


list_of_incs = []


@app.route('/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(commands=['check'])
def start(message):
    bot.send_message(message.chat.id, '<b>тут</b>', parse_mode='html')


@bot.message_handler(commands=['showbuttons'])
def show_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    one = types.KeyboardButton('инц')
    two = types.KeyboardButton('всеинц')
    markup.add(one, two, row_width=2)
    bot.send_message(message.chat.id, 'кнопки тут', reply_markup=markup)


@bot.message_handler(commands=['removebuttons'])
def remove_buttons(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'кнопок нет', reply_markup=markup)


@bot.message_handler()
def get_user_text(message):
    mes: str = message.text
    list_of_words_from_mes = mes.split(' ')

    if list_of_words_from_mes[0].lower() == 'инц':
        if list_of_words_from_mes.__len__() == 1:
            new_inc = create_inc(start=str(get_now()))
            bot.send_message(message.chat.id, print_inc(new_inc))
        elif not list_of_words_from_mes[1].isnumeric():
            des = ''
            for i in range(1, list_of_words_from_mes.__len__()):
                des += str(list_of_words_from_mes[i]) + ' '
            if list_of_words_from_mes[list_of_words_from_mes.__len__() - 1].lower() == 'ок':
                new_inc = create_inc(descr=des.removesuffix('ок '), start=str(get_now()), end=str(get_now()))
                bot.send_message(message.chat.id, print_inc(new_inc))
            else:
                new_inc = create_inc(descr=des, start=str(get_now()))
                bot.send_message(message.chat.id, print_inc(new_inc))
        elif check_inc_exist(int(list_of_words_from_mes[1]) - 1):
            if list_of_words_from_mes.__len__() > 2:
                des = ''
                for i in range(2, list_of_words_from_mes.__len__()):
                    des += str(list_of_words_from_mes[i]) + ' '
                if list_of_words_from_mes[list_of_words_from_mes.__len__() - 1].lower() == 'ок':
                    update_inc(inc_num=int(list_of_words_from_mes[1]) - 1, text=des.removesuffix('ок '), end=get_now())
                    bot.send_message(message.chat.id, print_inc(get_inc(inc_num=int(list_of_words_from_mes[1]) - 1)))
                else:
                    update_inc(inc_num=int(list_of_words_from_mes[1]) - 1, text=des)
                    bot.send_message(message.chat.id, print_inc(get_inc(inc_num=int(list_of_words_from_mes[1]) - 1)))
    elif list_of_words_from_mes[0].lower() == 'всеинц':
        bot.send_message(message.chat.id, str(print_list_of_incs(list_of_incs)))
    elif list_of_words_from_mes[0].lower() == 'всеинцудалить':
        clear_inc()
        bot.send_message(message.chat.id, 'все события удалены')


def create_inc(descr: Optional[str] = None, start: Optional[str] = None, end: Optional[str] = None):
    global last_inc_num
    global list_of_incs
    inc_num = last_inc_num + 1
    last_inc_num = inc_num
    new_inc = Inc(number=inc_num, description=descr, start_time=start, end_time=end)
    list_of_incs.append(new_inc)
    return new_inc


def get_inc(inc_num: int):
    return list_of_incs[inc_num]


def update_inc(inc_num, text: Optional[str] = None, end: Optional[str] = None):
    if (text is not None) & (text != ''):
        if list_of_incs[inc_num].description is None:
            list_of_incs[inc_num].description = text
        else:
            list_of_incs[inc_num].update = text
    if end is not None:
        list_of_incs[inc_num].end_time = end


def print_inc(inc):
    result = ''
    if inc.number is not None:
        result += str(inc.number) + ': '
    if inc.description is not None:
        result += inc.description + '\n'
    if inc.update is not None:
        result += 'дополн: ' + inc.update + '\n'
    if inc.start_time is not None:
        result += 'начало: ' + inc.start_time + '\n'
    if inc.end_time is not None:
        result += 'заверш: ' + inc.end_time + '\n'
    result += '\n'
    return result
    # return f'событие: {inc.number}' \
    #        f'\nописан: {inc.description}' \
    #        f'\nдополн: {inc.update}' \
    #        f'\nначало: {inc.start_time}' \
    #        f'\nзаверш: {inc.end_time}\n\n'


def get_now():
    return datetime.now().strftime('%d.%m %H:%M:%S')


def print_list_of_incs(list_of_incs):
    result = ''
    if list_of_incs.__len__() != 0:
        result = 'cписок: \n\n'
        for inc in list_of_incs:
            result += print_inc(inc)
    else:
        result = 'событий нет'
    return result


def check_inc_exist(num):
    return list_of_incs.__len__() > num


def clear_inc():
    list_of_incs.clear()


if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=WEB_HOOK_URL)
    app.run(host=APP_HOST, port=APP_PORT, debug=True)

# bot.infinity_polling(timeout=10, long_polling_timeout = 5)