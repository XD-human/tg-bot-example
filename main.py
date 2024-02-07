import telebot
from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

import liked_words
from wiktionary_parser import WiktionaryParser

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
liked_words.initialize()


@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(
        message.chat.id,
        "Привет! Я чат-бот словарь русского языка. "
        "Введи любое слово, чтобы определить его значение, или команду /help для справки.\n"
        "Ты можешь получить несколько значений слова, подкрепленных примерами.\n\n"
        "В основе работы бота лежит сайт https://ru.wiktionary.org/",
    )


@bot.message_handler(commands=["help"])
def help_user(message: Message):
    bot.send_message(
        message.chat.id,
        "Используй бота, чтобы узнать значение любого слова русского языка.\n"
        "Бот вернет все значения этого слова (их может быть даже больше 10 - как у слова 'слово'!).\n\n"
        "Команды:\n"
        "/start - Запуск чат-бота\n"
        "/help - Вспомогательная справка\n\n"
        "В основе работы бота лежит сайт https://ru.wiktionary.org/",
    )


@bot.message_handler()
def find_definition(message: Message):
    word = message.text

    if len(word.split()) > 1:
        bot.send_message(message.chat.id, "Нужно прислать одно слово, а не несколько")
        return None

    liked_words_keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Сохранить слово", callback_data=f"SAVE {word}")
    liked_words_keyboard.add(button)

    definitions = WiktionaryParser.get_wiktionary_definition(message.text)
    msg = f"Слово: `{word}`\n"
    i = 1
    if not definitions:
        bot.send_message(message.chat.id, f"Я не знаю слова {word}")
        return None

    for definition in definitions:
        msg += f"{i}. {definition.definition}\n"
        if definition.examples:
            "Примеры:\n"
            msg += '\n'.join([f"- {example}" for example in definition.examples])
            msg += '\n'
        i += 1
    bot.send_message(
        message.chat.id,
        msg,
        reply_markup=liked_words_keyboard,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_message(call: telebot.types.CallbackQuery):
    command, *args = call.data.split()
    if command == "SAVE":
        word = args[0]
        liked_words.add_word(word)
        return None


bot.polling()
