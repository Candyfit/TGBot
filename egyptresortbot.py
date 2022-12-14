import telebot
import requests
import random
import sqlite3
from config import open_weather_token
from telebot import types
from datetime import date
from bs4 import BeautifulSoup as b

bot = telebot.TeleBot('token')


c_date = date.today()

with open('quiz','r',encoding='utf-8')as file:
    quiz = []
    for l in file:
        quiz.extend(file.readlines())


@bot.message_handler(commands=['start'])

def get_text_messages(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Погода в Египте', callback_data='request1')
    item2 = types.InlineKeyboardButton('Интересное о Египте', callback_data='request2')
    item3 = types.InlineKeyboardButton(f"Рейтинг отелей на {c_date}", callback_data='request3')
    item4 = types.InlineKeyboardButton('Связаться с менеджером', callback_data='request4')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, 'Привет, друг! Давай окунемся в мир Востока! '
                                          '\U0001F54C\U0001F9C6\U0001F3DD\U0001F42A\U0001F420\n', reply_markup=markup)

def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Оставь свой контактный номер +375(__)_______")
    bot.register_next_step_handler(message, reg_number)


def reg_number(message):
    global number
    number = message.text
    try:
        if len(number) == 9 and number.isdigit():

            conn = sqlite3.connect('record.db')
            cursor = conn.cursor()

            id_user = message.chat.id
            cursor.execute('''INSERT INTO record_bot(id_user,name,number) VALUES(?,?,?)''',(id_user, name, number))
            conn.commit()

            markup = types.InlineKeyboardMarkup(row_width=2)
            item13 = types.InlineKeyboardButton('Music 1', callback_data='request13')
            item14 = types.InlineKeyboardButton('Music 2', callback_data='request14')
            markup.add(item13, item14)

            bot.send_message(5061654499,
                             f"Прием-прием,{name} очень хочет отдохнуть в Египте!Позвони - {number}! \U0001F92A")

            bot.send_message(message.from_user.id, "Отлично! В скором времени с тобой свяжется наш специалист,"
                                                   "а пока послушай музыку, красота которой обладает непередаваемым восточным колоритом!", reply_markup=markup)
        else:
            raise Exception
    except Exception:
        bot.send_message(message.from_user.id, "Введи 9 цифр номера без пробелов +375(__)_______")
        bot.register_next_step_handler(message, reg_number)



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "request1":
        w = random.choice(quiz)
        bot.send_message(call.message.chat.id, f"Сейчас пришлю самую точную информацию о погоде!\nНо для начала ответь мне.\n\n{w}\U0001F914\U0001F4AD")
        bot.register_next_step_handler(call.message, get_weather)

    if call.data == "request3":
        markup = types.InlineKeyboardMarkup(row_width=2)
        item5 = types.InlineKeyboardButton('Шарм-эль-Шейх', callback_data='request5')
        item6 = types.InlineKeyboardButton('Хургада', callback_data='request6')
        markup.add(item5, item6)
        bot.send_message(call.message.chat.id, 'Рейтинг отелей какого курортного города?\U0001F914', reply_markup=markup)
    if call.data == "request2":
        markup = types.InlineKeyboardMarkup(row_width=1)
        item7 = types.InlineKeyboardButton('Памятка туристам', callback_data='request7')
        item8 = types.InlineKeyboardButton('Погода в Египте по месяцам', callback_data='request8')
        item9 = types.InlineKeyboardButton('Достопримечательности в Шарм-эль-Шейхе', callback_data='request9')
        item10 = types.InlineKeyboardButton('Достопримечательности В Хургаде', callback_data='request10')
        item11 = types.InlineKeyboardButton('Какой курорт в Египте самый лучший', callback_data='request11')
        item12 = types.InlineKeyboardButton('Удивительные факты о Египте', callback_data='request12')

        markup.add(item7, item8, item9,item10, item11, item12)
        bot.send_message(call.message.chat.id, '   У меня много интересного! \U0001F642 Выбирай:   ', reply_markup=markup)

    if call.data == "request4":
        conn = sqlite3.connect('record.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS record_bot(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            name TEXT,
            number TEXT)""")
        conn.commit()
        id_us = call.message.chat.id
        cursor.execute(f"SELECT id FROM record_bot WHERE id_user={id_us}")
        info = cursor.fetchone()
        if info is None:
            bot.send_message(call.message.chat.id, "Как тебя зовут?")
            bot.register_next_step_handler(call.message, reg_name)
        else:
            cursor.execute(f"""SELECT * FROM record_bot
                     WHERE id_user = {id_us}
                 """)
            gen_info = cursor.fetchone()

            markup = types.InlineKeyboardMarkup(row_width=2)
            item13 = types.InlineKeyboardButton('Music 1', callback_data='request13')
            item14 = types.InlineKeyboardButton('Music 2', callback_data='request14')
            markup.add(item13, item14)

            bot.send_message(call.message.chat.id, f"{gen_info[2]},скоро с тобой свяжемся! А сейчас предлагаю послушать музыку,"
                                                   f" красота которой обладает непередаваемым восточным колоритом!", reply_markup=markup)
            bot.send_message(5061654499, f"Прием-прием,{gen_info[2]} очень хочет отдохнуть в Египте!Позвони - {gen_info[3]}! \U0001F92A")

    if call.data == "request5":
        q = random.choice(quiz)
        bot.send_message(call.message.chat.id, f"Сейчас покажу актуальный рейтинг отелей.\nНо для начала ответь мне.\n\n{q}\U0001F914\U0001F4AD")
        bot.register_next_step_handler(call.message, top_hotels_sharm)

    if call.data == "request6":
        q = random.choice(quiz)
        bot.send_message(call.message.chat.id,
                         f"Сейчас покажу актуальный рейтинг отелей.\nНо для начала ответь мне.\n\n{q}\U0001F914\U0001F4AD")
        bot.register_next_step_handler(call.message, top_hotels_hurghada)


    if call.data == "request7":
        bot.send_message(call.message.chat.id, 'https://telegra.ph/Pamyatka-turistam-07-17')
    if call.data == "request8":
        bot.send_message(call.message.chat.id, 'https://telegra.ph/Pogoda-v-Egipte-po-mesyacam-07-12')
    if call.data == "request9":
        bot.send_message(call.message.chat.id, 'https://telegra.ph/Dostoprimechatelnosti-SHarm-ehl-SHejha-07-17')
    if call.data == "request10":
        bot.send_message(call.message.chat.id, 'https://telegra.ph/Dostoprimechatelnosti-Hurgady-07-17')
    if call.data == "request11":
        bot.send_message(call.message.chat.id, 'https://telegra.ph/Kakoj-kurort-v-Egipte-samyj-luchshij-07-17')
    if call.data == "request12":
        w = random.choice(quiz)
        bot.send_message(call.message.chat.id, w)

    if call.data == "request13":
        audio = open('Egyptian music_1.mp3', 'rb')
        bot.send_audio(call.message.chat.id, audio)

    if call.data == "request14":
        audio = open('Egyptian music_2.mp3', 'rb')
        bot.send_audio(call.message.chat.id, audio)



def top_hotels_hurghada(message):
    r = requests.get('https://tophotels.ru/hotels/12/4?cat=10_70th_9th_75th_9_23&sort=-rate')
    r2 = requests.get('https://tophotels.ru/hotels/12/4?cat=10_70th_9th_75th_9_23&sort=-rate')
    soup = b(r.text, 'html.parser')
    soup2 = b(r2.text, 'html.parser')
    hotels = soup.find_all('div', class_='catalogs-ttl')
    keys = [i.text for i in hotels]
    del keys[10:]
    rating = soup2.find_all('span', class_='page-ttls-hotel-rating rating-good')
    values = [i.text for i in rating]
    del values[10:]
    d = dict(zip(keys, values))

    h_rating = ''
    for k, v in d.items():
        h_rating += str(k + v) + '\n'
    bot.send_message(message.from_user.id,
                     f"\U0000203CРейтинг составлен на основе данных,\nполученных на www.tophotels.ru\U0000203C\n"
                     f"\nЛучшие отели Хургады:\n\n{h_rating}")


def top_hotels_sharm(message):
    r = requests.get('https://tophotels.ru/hotels/12/7?cat=10_9_23&sort=-popular')
    r2 = requests.get('https://tophotels.ru/hotels/12/7?cat=10_9_23&sort=-popular')
    soup = b(r.text, 'html.parser')
    soup2 = b(r2.text, 'html.parser')
    hotels = soup.find_all('div', class_='catalogs-ttl')
    keys = [i.text for i in hotels]
    del keys[10:]
    rating = soup2.find_all('span', class_='page-ttls-hotel-rating rating-good')
    values = [i.text for i in rating]
    del values[10:]
    d = dict(zip(keys, values))

    sorted_dict = {}
    sorted_keys = sorted(d, key=d.get)
    for w in sorted_keys:
        sorted_dict[w] = d[w]
    d.clear()

    sharm_rating = ''
    for k, v in sorted_dict.items():
        sharm_rating = str(k + v) + '\n' + sharm_rating
    bot.send_message(message.from_user.id, f"\U0000203CРейтинг составлен на основе данных,\nполученных на www.tophotels.ru\U0000203C\n"
                                           f"\nЛучшие отели Шарм-эль-Шейха:\n\n{sharm_rating}")




def get_weather(message):
    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Sharm el-Sheikh&appid={open_weather_token}&units=metric")
    r2 = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Hurghada&appid={open_weather_token}&units=metric")
    data = r.json()
    data2 = r2.json()

    code_to_smile = {
                "Clear": "Ясно \U00002600",
                "Clouds": "Облачно \U00002601",
                "Rain": "Дождь \U00002614",
                "Drizzle": "Дождь \U00002614",
                "Dust": "Песчаная буря \U0001F32C",
                "Mist": "Туман \U0001F32B"
            }

    weather_description = data["weather"][0]["main"]
    weather_description2 = data2["weather"][0]["main"]
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
        wd2 = code_to_smile[weather_description2]

    cur_weather = data["main"]["temp"]
    cur_weather2 = data2["main"]["temp"]

    bot.send_message(message.from_user.id, f"Текущая погода в Шарм-эль-Шейхе: {cur_weather}°C - {wd}\n"
                                            f"\n"
                                            f"Текущая погода в Хургаде: {cur_weather2}°C - {wd2}")



bot.polling(none_stop=True, interval=0)


