"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.

"""
import logging
from datetime import datetime

import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn',
        'password': 'python'
    }
}


def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(text)


def planet(update, context):
    planet_list = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sun', 'Moon']
    answer = f"Попробуйте написать /planet _Название-планеты_\n`Известные мне планеты: {', '.join(planet_list)}.`"
    query = update.message.text.split()[1]

    if len(context.args) == 0:
        return update.message.reply_text(answer, parse_mode="Markdown")

    if query not in planet_list:
        return update.message.reply_text(("`Планета не найдена`\n" + answer), parse_mode="Markdown")

    date = datetime.now().strftime("%Y/%m/%d")
    target = getattr(ephem, query)(date)
    target_position, target_position_full = ephem.constellation(target)
    answer = f"`Планета` {target.name} `сегодня в созвездии` {target_position}\n" \
             f"`Также известном как` {target_position_full}"

    update.message.reply_text(answer, parse_mode="Markdown")


def wordcount(update, context):
    update.message.reply_text(f"`{len(context.args)}`", parse_mode="Markdown")


def main():
    mybot = Updater("КЛЮЧ, КОТОРЫЙ НАМ ВЫДАЛ BotFather", request_kwargs=PROXY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler('planet', planet))
    dp.add_handler(CommandHandler('wordcount', wordcount))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
