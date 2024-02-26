
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
from telebot import types

# Создаем бота с токеном
bot = telebot.TeleBot("6597390183:AAFgX7oyGks2Z3bcMXFWga-LmRIT9Ttqaus")


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Выберите режим:")
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    keyboard.add(types.KeyboardButton('Локации'), types.KeyboardButton('Интересные места'))
    bot.send_message(message.chat.id, 'Выберите режим:', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Локации')
def mode_1(message):
    bot.reply_to(message, "Чтобы посмотреть локацию напишите: /locat")


@bot.message_handler(func=lambda message: message.text == 'Интересные места')
def mode_2(message):
    bot.reply_to(message, "Чтобы посмотреть интересные места напишите: /locations")


# Клавиатура для запроса геолокации
keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button = KeyboardButton(text="Отправить геолокацию", request_location=True)
keyboard.add(button)

API_KEY = 'bb8fb0a2-22df-4d8b-8fdb-69d9fd4e258d'

@bot.message_handler(commands=['locat'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Чтобы узнать достопримечательности, нажмите кнопку ниже.", reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    # Отправка запроса к 2GIS API для получения достопримечательностей
    attractions_url = f"https://catalog.api.2gis.com/3.0/items?&key={API_KEY}&radius=1000&point={longitude},{latitude}&sort_point={longitude},{latitude}&sort=distance&fields=items.point,items.name,items.description"
    attractions_response = requests.get(attractions_url)
    attractions_data = attractions_response.json()

    if attractions_data.get('meta', {}).get('code') == 200:
        attractions = attractions_data.get('result', {}).get('items', [])
        if attractions:
            bot.send_message(message.chat.id, "Достопримечательности:")
            for attraction in attractions:
                name = attraction.get('name', '')
                description = attraction.get('description', '')
                bot.send_message(message.chat.id, f"Название: {name}\nОписание: {description}")
        else:
            bot.send_message(message.chat.id, "Достопримечательности не найдены.")
    else:
        bot.send_message(message.chat.id, "Не удалось получить данные о достопримечательностях.")

@bot.message_handler(commands=['locations'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('Азово')
    button2 = types.KeyboardButton('Тара')
    button3 = types.KeyboardButton('Любино')
    button4 = types.KeyboardButton('Большеречье')
    button5 = types.KeyboardButton('Иссилькуль')
    button6 = types.KeyboardButton('Муромцево')
    button7 = types.KeyboardButton('Ачаир')
    button8 = types.KeyboardButton('Большие Уки')
    markup.add(button1, button2, button3, button4, button5, button6, button7, button8)
    bot.send_message(message.chat.id, "Привет! Вот интересные достопримечательности:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Азово':
        bot.send_message(message.chat.id,
                         "https://t.me/interesplaces/6")
    elif message.text == 'Тара':
        bot.send_message(message.chat.id,
                         "https://t.me/interesplaces/12")
    elif message.text == 'Любино':
        bot.send_message(message.chat.id,
                         "https://t.me/interesplaces/19")
    elif message.text == 'Большеречье':
        bot.send_message(message.chat.id,
                         "https://t.me/interesplaces/14")
    elif message.text == 'Иссилькуль':
        bot.send_message(message.chat.id,
                         "https://t.me/interesplaces/15")
    elif message.text == 'Муромцево':
        bot.send_message(message.chat.id,
                         "https://t.me/interesplaces/16")
    elif message.text == 'Ачаир':
        bot.send_message(message.chat.id,
                         "https://t.me/interesplaces/17")
    elif message.text == 'Большие Уки':
        bot.send_message(message.chat.id,
                         "https://t.me/interesplaces/18")
    else:
        bot.send_message(message.chat.id, "Я не понимаю вашего сообщения.")

        # Запускаем бота
bot.polling()