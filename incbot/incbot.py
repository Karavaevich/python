from typing import Optional

import telebot
import flask
import time
import logging
from telebot import types
from datetime import datetime



# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

API_TOKEN = '6402634448:AAGq1MQC1OtiXPxW9ybdWiCLrG_pBAQaEQI'
WEBHOOK_HOST = '5.252.21.134'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '5.252.21.134'  # In some VPS you may need to put here the IP addr
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)
WEBHOOK_SSL_CERT = '/ssl_for_bot/webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/ssl_for_bot/webhook_pkey.pem'  # Path to the ssl private key

APP_HOST = '127.0.0.1'
APP_PORT = 8444
WEB_HOOK_URL = 'https://fac9-217-107-125-211.ngrok.io'

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)

last_inc_num = 0


class Inc:
    def __init__(self, number: int, start_time: str, description: Optional[str] = None, updates: Optional[dict] = {},
                 end_time: Optional[str] = None):
        self.number: int = number
        self.description: str = description
        self.updates: dict = updates
        self.start_time: str = start_time
        self.end_time: str = end_time


dict_of_incs = dict()


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
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
        elif check_inc_exist(int(list_of_words_from_mes[1])):
            if list_of_words_from_mes.__len__() == 2:
                bot.send_message(message.chat.id, print_inc(get_inc(inc_num=int(list_of_words_from_mes[1]))))
            if list_of_words_from_mes.__len__() > 2:
                if list_of_words_from_mes[2].lower() == 'удалить':
                    bot.send_message(message.chat.id, print_inc(dict_of_incs.pop(int(list_of_words_from_mes[1]))))
                des = ''
                for i in range(2, list_of_words_from_mes.__len__()):
                    des += str(list_of_words_from_mes[i]) + ' '
                if list_of_words_from_mes[list_of_words_from_mes.__len__() - 1].lower() == 'ок':
                    update_inc(inc_num=int(list_of_words_from_mes[1]), text=des.removesuffix('ок '), end=get_now())
                    bot.send_message(message.chat.id, print_inc(get_inc(inc_num=int(list_of_words_from_mes[1]))))
                else:
                    update_inc(inc_num=int(list_of_words_from_mes[1]), text=des)
                    bot.send_message(message.chat.id, print_inc(get_inc(inc_num=int(list_of_words_from_mes[1]))))
    elif list_of_words_from_mes[0].lower() == 'всеинц':
        bot.send_message(message.chat.id, str(print_dict_of_incs(dict_of_incs)))
    elif list_of_words_from_mes[0].lower() == 'всеинцудалить':
        clear_inc()
        bot.send_message(message.chat.id, 'все события удалены')


def create_inc(descr: Optional[str] = None, start: Optional[str] = None, end: Optional[str] = None):
    global last_inc_num
    global map_of_incs
    inc_num = last_inc_num + 1
    last_inc_num = inc_num
    new_inc = Inc(number=inc_num, description=descr, start_time=start, end_time=end)
    dict_of_incs[inc_num] = new_inc
    return new_inc


def get_inc(inc_num: int):
    return dict_of_incs[inc_num]


def update_inc(inc_num, text: Optional[str] = None, end: Optional[str] = None):
    if (text is not None) & (text != ''):
        if dict_of_incs[inc_num].description is None:
            dict_of_incs[inc_num].description = text
        else:
            dict_of_incs[inc_num].updates[get_now()] = text
    if end is not None:
        dict_of_incs[inc_num].end_time = end


def print_inc(inc):
    result = ''
    if inc.description is not None:
        result += inc.description + '\n'
    if inc.start_time is not None:
        result += 'начало: ' + inc.start_time + '\n'
    if inc.updates.__len__() != 0:
        for update in inc.updates:
            result += 'дополн: ' + update + ' ' + inc.updates[update] + '\n'
    if inc.end_time is not None:
        result += 'заверш: ' + inc.end_time + '\n'
    if inc.number is not None:
        result += 'админу: ' + str(inc.number) + '\n'
    result += '\n'
    return result


def get_now():
    return datetime.now().strftime('%d.%m %H:%M:%S')


def get_now_short():
    return datetime.now().strftime('%H:%M')


def print_dict_of_incs(dict_of_incs):
    result = ''
    if dict_of_incs.__len__() != 0:
        result = 'cписок: \n\n'
        for inc_num in dict_of_incs.keys():
            result += print_inc(dict_of_incs[inc_num])
    else:
        result = 'событий нет'
    return result


def check_inc_exist(num):
    if num in dict_of_incs:
        return True
    else:
        return False


def clear_inc():
    dict_of_incs.clear()


if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=True)