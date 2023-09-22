import traceback
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

# pppincbot
# API_TOKEN = '6449337054:AAE_Pa6ipXDR44502Dy9lhj_LY5hIuxGXQY'
# KVAtestbot
API_TOKEN = '6402634448:AAGBaX0Iqn5U0EFyQrN62posnLWri7p7rPo'

WEBHOOK_HOST = '94.139.255.242'
# pppincbot
# WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
# KVAtestbot
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '192.168.0.178'  # In some VPS you may need to put here the IP addr
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)
WEBHOOK_SSL_CERT = '/ssl_for_bot/webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/ssl_for_bot/webhook_pkey.pem'  # Path to the ssl private key

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)

stable = True

last_inc_num = 0
need_delete_commands = False


class Inc:
    def __init__(self, number: int, start_time: str, description: Optional[str] = None, updates=None,
                 tks: Optional[str] = None, end_time: Optional[str] = None):
        if updates is None:
            updates = {}
        self.number: int = number
        self.description: str = description
        self.updates: dict = updates
        self.tks: str = tks
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


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'привет\n/check\n/help')


@bot.message_handler(commands=['check'])
def start(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'все ок')
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(message.chat.id, 'я тут, но не могу удалять команды чтобы не захламлять чат\n+проверь что я '
                                          'админ иначе не смогу читать обычные сообщения')


@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, '''
бот отслеживает ключевые слова и регистрирует события

создать событие:
“инц” - присвоится только номер и время начала
“инц ТЕКСТ” - присвоится номер, время начала и описание

обновить событие:
“инц НОМЕР ТЕКСТ” - присвоится описание, если оно было пустое, иначе добавится новое дополнение со временем

добавить номер ткс в событие:
“инц ткс НОМЕР_ТКС” - событию присвоится номер ткс

закрыть событие:
“инц НОМЕР <ТЕКСТ> ок” - событию присвоится время завершения, текст опционален, если указан - запишется либо в описание, либо в дополнения
*событие можно закрыть сразу при открытии, дописав “ок” в конце сообщения

вывести событие:
“инц НОМЕР” - вывести конкретное событие
“всеинц” - вывести список всех событий одним сообщением

очистить события:
“инц НОМЕР удалить” - удалить конкретное событие
“всеинцудалить” - все события очистятся и счетчик сбросится
    ''')


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
    chat_id_to_reply = message.chat.id
    mes: str = message.text
    list_of_words_from_mes = mes.split(' ')

    try:
        if list_of_words_from_mes[0].lower() == 'инц':
            if list_of_words_from_mes.__len__() == 1:
                new_inc = create_inc(start=str(get_now()))
                reply(chat_id=chat_id_to_reply, message_id=message.message_id, text=print_inc(new_inc))
            elif not list_of_words_from_mes[1].isnumeric():
                des = ''
                for i in range(1, list_of_words_from_mes.__len__()):
                    des += str(list_of_words_from_mes[i]) + ' '
                if list_of_words_from_mes[list_of_words_from_mes.__len__() - 1].lower() == 'ок':
                    new_inc = create_inc(descr=des.removesuffix('ок '), start=str(get_now()), end=str(get_now()))
                    reply(chat_id=chat_id_to_reply, message_id=message.message_id, text=print_inc(new_inc))
                else:
                    new_inc = create_inc(descr=des, start=str(get_now()))
                    reply(chat_id=chat_id_to_reply, message_id=message.message_id, text=print_inc(new_inc))
            elif check_inc_exist(int(list_of_words_from_mes[1])):
                if list_of_words_from_mes.__len__() == 2:
                    reply(chat_id=chat_id_to_reply,
                          message_id=message.message_id,
                          text=print_inc(get_inc(inc_num=int(list_of_words_from_mes[1]))))
                elif list_of_words_from_mes.__len__() > 2:
                    if list_of_words_from_mes[2].lower() == 'удалить':
                        reply(chat_id=chat_id_to_reply,
                              message_id=message.message_id,
                              text='удалено событие:\n' + print_inc(dict_of_incs.pop(int(
                                  list_of_words_from_mes[1]))))
                    elif list_of_words_from_mes[2].lower() == 'ткс':
                        if list_of_words_from_mes.__len__() > 3:
                            if list_of_words_from_mes[3].isnumeric():
                                update_inc(inc_num=int(list_of_words_from_mes[1]), tks_num=list_of_words_from_mes[3])
                                reply(chat_id=chat_id_to_reply,
                                      message_id=message.message_id,
                                      text=print_inc(get_inc(inc_num=int(list_of_words_from_mes[1])), short=True))
                    else:
                        des = ''
                        for i in range(2, list_of_words_from_mes.__len__()):
                            des += str(list_of_words_from_mes[i]) + ' '
                        if list_of_words_from_mes[list_of_words_from_mes.__len__() - 1].lower() == 'ок':
                            update_inc(inc_num=int(list_of_words_from_mes[1]),
                                       text=des.removesuffix('ок '),
                                       end=get_now())
                            reply(chat_id=chat_id_to_reply,
                                  message_id=message.message_id,
                                  text=print_inc(get_inc(inc_num=int(list_of_words_from_mes[1])), short=True))
                        else:
                            update_inc(inc_num=int(list_of_words_from_mes[1]), text=des)
                            reply(chat_id=chat_id_to_reply,
                                  message_id=message.message_id,
                                  text=print_inc(get_inc(inc_num=int(list_of_words_from_mes[1])), short=True))
        elif list_of_words_from_mes[0].lower() == 'всеинц':
            reply(chat_id=chat_id_to_reply, message_id=message.message_id, text=str(print_dict_of_incs()))
        elif list_of_words_from_mes[0].lower() == 'всеинцудалить':
            clear_inc()
            reply(chat_id=chat_id_to_reply, message_id=message.message_id, text='все события удалены')
        elif list_of_words_from_mes[0].lower() == 'удалятькоманды':
            set_need_delete_commands(True)
            bot.send_message(chat_id_to_reply, 'команды будут удаляться')
        elif list_of_words_from_mes[0].lower() == 'неудалятькоманды':
            set_need_delete_commands(False)
            bot.send_message(chat_id_to_reply, 'команды не будут удаляться')
    except:
        bot.send_message(chat_id_to_reply, 'ошибка')

    if message.reply_to_message.message_id == 1023:
        bot.send_message(chat_id_to_reply, "catched!", reply_to_message_id=message.message_id)


def reply(chat_id: str, message_id: int, text: str):
    bot.send_message(chat_id, text)
    if need_delete_commands:
        bot.delete_message(chat_id=chat_id, message_id=message_id)


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


def update_inc(inc_num, text: Optional[str] = None, tks_num: Optional[str] = None, end: Optional[str] = None):
    if (text is not None) & (text != ''):
        if dict_of_incs[inc_num].description is None:
            dict_of_incs[inc_num].description = text
        else:
            dict_of_incs[inc_num].updates[get_now_short()] = text
    if tks_num is not None:
        dict_of_incs[inc_num].tks = tks_num
    if end is not None:
        dict_of_incs[inc_num].end_time = end


def print_inc(inc: Inc, short: bool = False):
    result = ''
    if inc.description is not None:
        result += inc.description + '\n'
    if inc.tks is not None:
        result += 'ткс: 8 (800) 555-55-52,' + inc.tks + '#\n'
    if inc.start_time is not None:
        result += 'начало: ' + inc.start_time + '\n'
    if inc.updates.__len__() != 0:
        if short:
            last_key = list(inc.updates)[-1]
            result += 'статус: ' + inc.updates[last_key] + '\n'
        else:
            for update in inc.updates:
                result += update + ' ' + inc.updates[update] + '\n'
    if inc.end_time is not None:
        result += 'заверш: ' + inc.end_time + '\n'
    if inc.number is not None:
        result += 'админу: ' + str(inc.number) + '\n'
    result += '\n'
    return result


def get_now():
    return datetime.now().strftime('%d.%m %H:%M')


def get_now_short():
    return datetime.now().strftime('%H:%M:%S')


def print_dict_of_incs():
    result = ''
    if dict_of_incs.__len__() != 0:
        result = 'cписок: \n\n'
        for inc_num in dict_of_incs.keys():
            result += print_inc(dict_of_incs[inc_num])
    else:
        result = 'событий нет'
    return result


def set_need_delete_commands(flag: bool):
    global need_delete_commands
    need_delete_commands = flag


def check_inc_exist(num):
    if num in dict_of_incs:
        return True
    else:
        return False


def clear_inc():
    global last_inc_num
    dict_of_incs.clear()
    last_inc_num = 0


if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=True)
