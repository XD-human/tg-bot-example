import telebot
from telebot.types import (
    Message,
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
        
        "Избранные слова: ты можешь сохранять слова, чтобы потом вызвать их из памяти.\n"
        "/save {слово} - сохранить слово в избранные.\n"
        "/delete {слово} - удалить слово из твоих избранных.\n"
        "/liked - вызвать твои избранные слова из памяти.\n\n"
        
        "В основе работы бота лежит сайт https://ru.wiktionary.org/",
    )


@bot.message_handler(commands=["save"])
def save_word(message: Message):
    word = message.text.removeprefix("/save").strip()
    result = liked_words.try_add_word(message.chat.id, word)
    if result.succeed:
        bot.send_message(
            message.chat.id,
            f"Слово {word} добавлено в избранные."
        )
    else:
        bot.send_message(
            message.chat.id,
            f"Слово {word} не удалось добавить в избранные: {result.err_message}"
        )
    return None


@bot.message_handler(commands=["delete"])
def delete_word(message: Message):
    word = message.text.removeprefix("/delete").strip()
    result = liked_words.try_remove_word(message.chat.id, word)
    if result.succeed:
        bot.send_message(
            message.chat.id,
            f"Слово {word} удалено из избранных."
        )
    else:
        bot.send_message(
            message.chat.id,
            f"Слово {word} не удалось добавить в избранные: {result.err_message}"
        )
    return None


@bot.message_handler(commands=["liked"])
def get_liked_words(message: Message):
    words = liked_words.get_words(message.chat.id)
    words_string = "\n".join([f"{i + 1}. {word}" for i, word in enumerate(words)])
    bot.send_message(
        message.chat.id,
        f"Ваши избранные слова:\n"
        f"{words_string}"
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
        result = liked_words.try_add_word(call.message.chat.id, word)

        if result.succeed:
            bot.send_message(
                call.message.chat.id,
                f"Слово {word} добавлено в избранные."
            )
        else:
            bot.send_message(
                call.message.chat.id,
                f"Слово {word} не удалось добавить в избранные: {result.err_message}"
            )

        return None


bot.polling()
