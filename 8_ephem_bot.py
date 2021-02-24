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
    count = len(context.args)
    update.message.reply_text(f"`{count}`", parse_mode="Markdown")


def next_full_moon(update, context):
    date = datetime.now()

    if len(context.args) != 0:
        date = datetime.strptime(context.args[0].strip(), "%Y-%m-%d")

    full_moon_date = ephem.next_full_moon(date)
    update.message.reply_text(f"`Дата отсчета {date.date()}`\n"
                              f"`Следующее полнолуние:` {full_moon_date}",
                              parse_mode="Markdown")


def city_game(update, context):
    game = context.user_data.get('city_game')

    if game is None:
        game = CityGame()
        game.start_new_game()

    try:
        player_city = update.message.text.split()[1]
    except IndexError:
        answer = '`Введите после "Город" название города на русском языке.`\n' \
                 '`Если название города состоит из нескольких слов то разделяйте их дефисами "-"`'
        return update.message.reply_text(answer, parse_mode="Markdown")

    if not game.check_last_char(player_city):
        return update.message.reply_text(f"{player_city} `начинается не на` *{game.last_char}*", parse_mode="Markdown")

    if not game.check_city(player_city.lower()):
        return update.message.reply_text(
            f"`Города {player_city} нет в моей базе данных, попробуйте ещё раз`", parse_mode="Markdown"
        )

    new_city = game.get_city(player_city.lower())
    if new_city is None:
        username = update.effective_chat['username']
        answer = f'''
        *Поздравляю* {username}!\n
        `Городов начинающихся на` *{game.last_char}* `больше нет в моей базе данных.`\n
        `Вы выйграли назвав` *{game.score}* `города(ов).`
        '''
        context.user_data.pop('city_game')
        return update.message.reply_text(answer, parse_mode="Markdown")

    context.user_data['city_game'] = game
    last_char = player_city[-1].upper()
    new_last_char = game.last_char
    answer = f"`Ваш город:` {player_city} `заканчивается на букву` *{last_char}*\n" \
             f"`Мой ответ:` {new_city.capitalize()}.\n`Теперь Вам город на букву` *{new_last_char}*" \
             f"`На данный момент ваш счёт равен` *{game.score}*"

    update.message.reply_text(answer, parse_mode="Markdown")


def main():
    mybot = Updater("КЛЮЧ, КОТОРЫЙ НАМ ВЫДАЛ BotFather", request_kwargs=PROXY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler('planet', planet))
    dp.add_handler(CommandHandler('wordcount', wordcount))
    dp.add_handler(CommandHandler('next_full_moon', next_full_moon))
    dp.add_handler(MessageHandler(Filters.regex('^[Гг]ород'), city_game))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
