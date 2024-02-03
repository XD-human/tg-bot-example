# Русский словарь - чат-бот для Telegram
Этот бот для Telegram позволяет получать определения русских слов и примеры их применения
из Викисловаря (https://ru.wiktionary.org/) и отправлять их в чат.

## Установка
1. Клонируйте репозиторий бота на свой компьютер
    ```commandline
    git clone https://github.com/XD-human/tg-bot-example.git
    ```
2. Установите зависимости
    ```commandline
    pip install -r requirements.txt
    ```
3. Создайте файл `.env` и добавьте в него токен вашего бота для Telegram
   (полученного в Telegram от BotFather). Файл `.env` должен выглядеть следующим образом:
   ```python
   TOKEN = "YOUR_BOT_TOKEN"
   ```

## Использование
1. Для запуска бота используйте команду:
    ```commandline
    py main.py
    ```
2. Отправьте боту сообщение с доступной командой (см. ниже) или словом, 
определение которого вы хотите найти.
3. Бот отправит ответ на команды или определение слова (если слово было найдено).

### Команды
- /start - Начало работы чат-бота.
- /help - Вспомогательная справка о работе чат-бота.
