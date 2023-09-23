import collections
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
need_delete_commands = True
need_delete_related_messages_after_closing = True


class Inc:
    def __init__(self, number: int, start_time: str, reporter: str, description: Optional[str] = None, updates=None,
                 tks: Optional[str] = None, end_time: Optional[str] = None, messages=None):
        if messages is None:
            messages = []
        if updates is None:
            updates = {}
        self.number: int = number
        self.description: str = description
        self.updates: dict[collections.Iterable, dict] = updates
        self.tks: str = tks
        self.start_time: str = start_time
        self.reporter: str = reporter
        self.end_time: str = end_time
        self.messages: list = messages


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
“инц ТЕКСТ ок” - присвоится номер, описание, время начала+завершения

изменить событие:
ответить на любое из сообщений бота, связанного с событием, по след логике:
“ТЕКСТ” - присвоится описание, если оно было пустое, иначе добавится новое дополнение со временем
“ткс НОМЕР_ТКС” - событию присвоится номер ткс
“<ТЕКСТ> ок” - событию присвоится время завершения, текст опционален, если указан - запишется либо в описание, либо в дополнения
"удалить" - удалить выбранное событие

вывести события:
“всеинц” - вывести список всех событий одним сообщением

очистить события:
“всеинцудалить” - все события очистятся и счетчик сбросится

опции:
"удалятькоманды / неудалятькоманды" - удалять ли команды(сообщения) пользователя
"удалятьсвязанные / неудалятьсвязанные" - удалять ли все предыдущие собщения бота по событию при его закрытии/удалении
    ''')


@bot.message_handler()
def get_user_text(message):
    current_chat_id = message.chat.id
    message_from_user: str = message.text
    message_id_from_user = message.message_id
    user = '@' + message.from_user.username
    list_of_words_from_mes = message_from_user.split(' ')

    # try:

    if list_of_words_from_mes[0].lower() == 'инц':

        if list_of_words_from_mes.__len__() == 1:
            new_inc = create_inc(start_datetime=str(get_now()), reporter=user)
            add_mes_id_to_inc = reply(chat_id=current_chat_id, message_id=message_id_from_user, text=print_inc(new_inc))
            new_inc.messages.append(add_mes_id_to_inc)

        else:
            des = message_from_user[4:]

            if des.lower().endswith(' ок'):
                des_for_inc = des[:-3]
                new_inc = create_inc(descr=des_for_inc, start_datetime=str(get_now()), end=str(get_now()), reporter=user)
                add_mes_id_to_inc = reply(chat_id=current_chat_id,
                                          message_id=message_id_from_user,
                                          text=print_inc(new_inc))
                new_inc.messages.append(add_mes_id_to_inc)

            else:
                new_inc = create_inc(descr=des, start_datetime=str(get_now()), reporter=user)
                add_mes_id_to_inc = reply(chat_id=current_chat_id,
                                          message_id=message_id_from_user,
                                          text=print_inc(new_inc))
                new_inc.messages.append(add_mes_id_to_inc)

    elif is_update_command(message):
        inc_num_from_command = get_inc_by_message(message.reply_to_message.message_id)
        add_mes_id_to_inc = None

        if message_from_user.lower() == 'удалить':
            delete_related_messages(chat_id=current_chat_id, inc_num=inc_num_from_command)
            dict_of_incs.pop(inc_num_from_command)
            bot.delete_message(chat_id=current_chat_id, message_id=message_id_from_user)

        elif is_tks_update_command(list_of_words_from_mes):
            update_inc(inc_num=int(inc_num_from_command), tks_num=list_of_words_from_mes[1], reporter=user)
            add_mes_id_to_inc = reply(chat_id=current_chat_id, message_id=message_id_from_user,
                                      text=print_inc(get_inc(inc_num=inc_num_from_command), short=True))

        else:

            if list_of_words_from_mes[-1].lower() == 'ок':
                update_inc(inc_num=inc_num_from_command, text=message_from_user[:-3], end=get_now(), reporter=user)
                add_mes_id_to_inc = reply(chat_id=current_chat_id,
                                          message_id=message_id_from_user,
                                          text='завершено:\n' + print_inc(get_inc(inc_num=inc_num_from_command)))

                if need_delete_related_messages_after_closing:
                    delete_related_messages(chat_id=current_chat_id, inc_num=inc_num_from_command)

            else:
                update_inc(inc_num=inc_num_from_command, text=message_from_user, reporter=user)
                add_mes_id_to_inc = reply(chat_id=current_chat_id,
                                          message_id=message_id_from_user,
                                          text=print_inc(get_inc(inc_num=inc_num_from_command), short=True))

        if check_inc_exist(inc_num_from_command):
            get_inc(inc_num=inc_num_from_command).messages.append(add_mes_id_to_inc)

    elif message_from_user.lower() == 'всеинц':
        reply(chat_id=current_chat_id, message_id=message_id_from_user, text=str(print_dict_of_incs()))

    elif message_from_user.lower() == 'всеинцудалить':
        clear_inc(current_chat_id)
        reply(chat_id=current_chat_id, message_id=message_id_from_user, text='все события удалены')

    elif message_from_user.lower() == 'удалятькоманды':
        set_need_delete_commands(True)
        bot.send_message(current_chat_id, 'команды пользователя будут удаляться')

    elif message_from_user.lower() == 'неудалятькоманды':
        set_need_delete_commands(False)
        bot.send_message(current_chat_id, 'команды пользователя не будут удаляться')

    elif message_from_user.lower() == 'удалятьсвязанные':
        set_need_delete_commands(True)
        bot.send_message(current_chat_id, 'предыдущие собщения бота по событию при его закрытии/удалении будут '
                                          'удаляться')

    elif message_from_user.lower() == 'неудалятьсвязанные':
        set_need_delete_commands(False)
        bot.send_message(current_chat_id, 'предыдущие собщения бота по событию при его закрытии/удалении не будут '
                                          'удаляться')


def is_tks_update_command(lst: list[str]) -> bool:
    if lst[0].lower() == 'ткс':
        if lst.__len__() == 2:
            if lst[1].isnumeric():
                return True
    return False


def is_update_command(message: telebot.types.Message) -> bool:
    if message.reply_to_message is not None:
        if get_inc_by_message(message.reply_to_message.message_id) > 0:
            return True
        return False


def reply(chat_id: str, message_id: int, text: str) -> int:
    new_mes_id_for_adding_to_inc = bot.send_message(chat_id, text).message_id
    if need_delete_commands:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    return new_mes_id_for_adding_to_inc


def create_inc(start_datetime: str, reporter: str, descr: Optional[str] = None, end: Optional[str] = None) -> Inc:
    global last_inc_num
    inc_num = last_inc_num + 1
    last_inc_num = inc_num
    new_inc = Inc(number=inc_num, description=descr, start_time=start_datetime, end_time=end, reporter=reporter)
    dict_of_incs[inc_num] = new_inc
    return new_inc


def delete_related_messages(chat_id: str, inc_num: int):
    bot_messages = get_inc(inc_num=inc_num).messages
    for bot_message in bot_messages:
        bot.delete_message(chat_id=chat_id, message_id=bot_message)
    bot_messages.clear()


def get_inc(inc_num: int) -> Inc:
    return dict_of_incs[inc_num]


def update_inc(inc_num, reporter: str, text: Optional[str] = None, tks_num: Optional[str] = None, end: Optional[str] = None):
    if (text is not None) & (text != ''):
        if dict_of_incs[inc_num].description is None:
            dict_of_incs[inc_num].description = text
        else:
            new_update_time = get_now_short()
            dict_of_incs[inc_num].updates[new_update_time] = {}
            dict_of_incs[inc_num].updates[new_update_time][reporter] = text
    if tks_num is not None:
        dict_of_incs[inc_num].tks = tks_num
    if end is not None:
        dict_of_incs[inc_num].end_time = end


def print_inc(inc: Inc, short: bool = False):
    result = ''
    if inc.reporter is not None:
        result += 'от ' + inc.reporter + '\n'
    if inc.description is not None:
        result += inc.description + '\n'
    if inc.tks is not None:
        result += 'ткс: 8 (800) 555-55-52,' + inc.tks + '#\n'
    if inc.start_time is not None:
        result += 'начало: ' + inc.start_time + '\n'
    if inc.updates.__len__() != 0:
        if short:
            last_update_key = list(inc.updates)[-1]
            last_update_user = list(inc.updates[last_update_key].keys())[0]
            last_update_text = inc.updates[last_update_key][last_update_user]
            result += last_update_user + ': ' + last_update_text + '\n'
        else:
            for update in inc.updates:
                for text in update:
                    result += str(update) + ' ' + inc.updates[update][text] + '\n'
    if inc.end_time is not None:
        result += 'заверш: ' + inc.end_time + '\n'
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


def get_inc_by_message(mes_id: int) -> int:
    for inc in dict_of_incs.keys():
        if dict_of_incs[inc].messages.__contains__(mes_id):
            return dict_of_incs[inc].number
    return 0


def clear_inc(chat_id):
    global last_inc_num
    for inc in dict_of_incs.keys():
        delete_related_messages(chat_id=chat_id, inc_num=inc)
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
