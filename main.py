from random import randint
import os
from telebot import types
import telebot
from pyCryptoPayAPI import pyCryptoPayAPI


APIS_DIR = "./apis/"
TG_API_TOKEN = open(f"{APIS_DIR}tg_api_token", 'r').readline()
PAYMENT_API_TOKEN = open(f"{APIS_DIR}payment_api_token", 'r').readline()
ADMIN_CHAT_ID = int(open(f"{APIS_DIR}admin_chat_id", 'r').readline())
DATA_DIR = "./data/"
TRASH_DIR = "./trash/"
INFO = "Вы можете получить случайную картинку космоса.\n\nКоманды:\n/start - начать работу с ботом\n/get - получить случайную картинку\n/pay - пожертвовать 1, 10 или 100 TON"
BUY = False
COST = 0
files = []
bot = telebot.TeleBot(TG_API_TOKEN)
crypto = pyCryptoPayAPI(api_token=PAYMENT_API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(msg):
    bot.send_message(
        msg.chat.id, 'Добро пожаловать!\n{INFO}'.format(INFO=INFO))


@bot.message_handler(commands=['pay'])
def pay(msg):
    markup = types.InlineKeyboardMarkup()

    invoice_1TON = crypto.create_invoice(asset="TON", amount=1)
    invoice_10TON = crypto.create_invoice(asset="TON", amount=10)
    invoice_100TON = crypto.create_invoice(asset="TON", amount=100)

    btn_1TON = types.InlineKeyboardButton(
        text="1 TON", url=invoice_1TON['pay_url'])
    btn_10TON = types.InlineKeyboardButton(
        text="10 TON", url=invoice_10TON['pay_url'])
    btn_100TON = types.InlineKeyboardButton(
        text="100 TON", url=invoice_100TON['pay_url'])

    markup.add(btn_1TON)
    markup.add(btn_10TON)
    markup.add(btn_100TON)

    bot.send_message(
        msg.chat.id, "Выберите сумму пожертвования:", reply_markup=markup)


@bot.message_handler(commands=['get'])
def buy(msg):
    try:
        files = [f for f in os.listdir(
            DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
        if len(files) == 0:
            bot.send_message(
                msg.chat.id, "Извините, изображения временно отсутствуют.\nЯ оповестил владельца об отсутствии изображений.\nПопробуйте позже.")
            bot.send_message(ADMIN_CHAT_ID, "Images not found")
        else:
            idx = randint(0, len(files) - 1)
            image = open(DATA_DIR + files[idx], 'rb')

            markup = types.InlineKeyboardMarkup()

            invoice_1TON = crypto.create_invoice(asset="TON", amount=1)
            invoice_10TON = crypto.create_invoice(asset="TON", amount=10)
            invoice_100TON = crypto.create_invoice(asset="TON", amount=100)

            btn_1TON = types.InlineKeyboardButton(
                text="1 TON", url=invoice_1TON['pay_url'])
            btn_10TON = types.InlineKeyboardButton(
                text="10 TON", url=invoice_10TON['pay_url'])
            btn_100TON = types.InlineKeyboardButton(
                text="100 TON", url=invoice_100TON['pay_url'])

            markup.add(btn_1TON)
            markup.add(btn_10TON)
            markup.add(btn_100TON)

            bot.send_photo(msg.chat.id, image, reply_markup=markup)

            os.replace(DATA_DIR + files[idx], TRASH_DIR + files[idx])
            files = [f for f in os.listdir(
                DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
    except FileNotFoundError as err:
        bot.send_message(
            msg.chat.id, "Извините, изображения временно отсутствуют.\nЯ оповестил владельца об отсутствии изображений.\nПопробуйте позже.")
        bot.send_message(ADMIN_CHAT_ID, f"Images not found\nerror: {err}")
    except Exception as err:
        bot.send_message(msg.chat.id, "unexpected error")
        bot.send_message(ADMIN_CHAT_ID, f"unexpected error\nerror: {err}")

# @bot.message_handler(commands=['get_chat_id'])
# def test(msg):
    # bot.send_message(msg.chat.id, f"{msg.chat.id}")


@bot.message_handler(content_types=['text'])
def text(msg):
    bot.send_message(
        msg.chat.id, "Извините, Я не понял что вы сказали\n\nКоманды:\n/start - начать работу с ботом\n/get - получить случайную картинку\n/pay - пожертвовать 1, 10 или 100 TON")


if __name__ == "__main__":
    bot.infinity_polling()
