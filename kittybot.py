from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater
from dotenv import load_dotenv

import requests
import os
import logging

load_dotenv()

URL = 'https://api.thecatapi.com/v1/images/search'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

def say_hi(update, context):
    # Получаем информацию о чате, из которого пришло сообщение,
    # и сохраняем в переменную chat
    chat = update.effective_chat
    # В ответ на любое текстовое сообщение 
    # будет отправлено 'Привет, я KittyBot!'
    context.bot.send_message(chat_id=chat.id, text='Привет, я KittyBot!')

def wake_up(update, context):
    chat = update.effective_chat
    first_name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id = chat.id,
        text = f'Ну здравствуй, {first_name}, посмотри, какого котика я тебе нашёл!',
        reply_markup = button
        )
    context.bot.send_photo(chat.id, get_new_image())

def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        # Печатать информацию в консоль теперь не нужно:
        # всё необходимое будет в логах
        # print(error)
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat 

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())

def main():
    auth_token = os.getenv('TOKEN_TL')

    # bot = Bot(token = auth_token)
    # chat_id = '644398715'
    updater = Updater(token=auth_token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()