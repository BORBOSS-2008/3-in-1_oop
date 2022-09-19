#!/usr/bin/env python
############################################################################
#
#   PROJECT_08 by the Team:
#
############################################################################

import requests
class Finance():

#     def __init__(self, currency='usd'):
#         self.currency = str.upper(currency)

    def get_data(self):
        api_cbr = 'https://www.cbr-xml-daily.ru/daily_json.js'
        res = requests.get(api_cbr)
        data = res.json()
        return data['Valute']


import telebot
import random
from telebot import types
import pandas as pd
import wikipedia
import langdetect
from datetime import datetime
class bot_facts:
    def __init__(self):
        self._token = '5626409380:AAFFhkrJuBCSxUiYM4BmWWODbUQte6W2hPs'
        self.path_type = 'start'
        self.open_weather_token = '5a5d0ebdb50eafbc058671d8e39505d6'
#     def load_facts(self):
#         f = open(self._facts_dir, 'r', encoding='UTF-8')
#         self.facts = f.read().split('\n')
#         f.close()
#     def load_thinks(self):
#         f = open(self._thinks_dir, 'r', encoding='UTF-8')
#         self.thinks  = f.read().split('\n')
#         f.close()
    def bot_create(self):
        self.bot = telebot.TeleBot(self._token)
    def main(self):        
        self.bot_create()
        @self.bot.message_handler(commands=["start"])
        def start(m, res=False):
                # Добавляем две кнопки
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

                
                markup.add(types.KeyboardButton("Курсы валют"))
                markup.add(types.KeyboardButton("Вики"))
                markup.add(types.KeyboardButton("Прогноз погоды"))
                self.markup = markup
                self.bot.send_message(m.chat.id, 'Нажми кнопку для получения курса валют',  reply_markup=markup)

        # Получение сообщений от юзера
        @self.bot.message_handler(content_types=["text"])
        def handle_text(message):
            # Если юзер прислал 1, выдаем ему случайный факт
            fn = Finance()
            cur = pd.DataFrame(fn.get_data())
            if message.text == 'Курсы валют':
#                 self.bot.send_message(message.chat.id, "ok")
                
#                 a = telebot.types.ReplyKeyboardRemove()
                
                markup_2=types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup_2.add('Назад')
                for i in cur:
                    markup_2.add(types.KeyboardButton(cur[i]['Name']))
                self.path_type = 'cur'
                self.bot.send_message(message.chat.id, 'Выберите валюту',  reply_markup=markup_2)
            elif message.text == 'Назад':
                self.path_type = 'start'
                self.bot.send_message(message.chat.id, 'Нажми кнопку для получения курса валют',  reply_markup=self.markup)
            elif message.text == 'Вики':
                markup_3=types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup_3.add('Назад')
                self.path_type = 'wiki'
                self.bot.send_message(message.chat.id, 'Введите текст',  reply_markup=markup_3)
            elif message.text == 'Прогноз погоды':
                markup_3=types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup_3.add('Назад')
                self.path_type = 'weather'
                self.bot.send_message(message.chat.id, 'Введите город',  reply_markup=markup_3)
            else:
                if self.path_type == 'cur':
                    for i in cur:
                        if message.text==cur[i]["Name"]:
                            cur_v = 1
                            answer = str(cur[i]['Value'] / cur[i]['Nominal']) + ' рублей'
                elif self.path_type == 'wiki':
                    try:
                        if message.text.lower()[0] in 'йцукенгшщзхъфывапролджэячсмитьбюё':
                            wikipedia.set_lang('ru')
                        elif message.text.lower()[0] in 'qwertyuiopasdfghjklzxcvbnm':
                            wikipedia.set_lang('en')
                        wk = wikipedia.page(message.text)
                        answer = wk.content[:1000]
                    except:
                        answer = 'Не найдено такой страницы'
                elif self.path_type == 'weather':
                    try: 
                        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                     params={'q': message.text, 'units': 'metric', 'lang': 'ru', 'APPID': self.open_weather_token})
                        data = res.json()
                        answer = "conditions: " + str(data['weather'][0]['description']) +'\n' +\
                        "temp: " + str(data['main']['temp'])+'\n' +\
                        "temp_min: " + str(data['main']['temp_min'])+'\n' +\
                        "temp_max: " + str(data['main']['temp_max'])
                    except Exception as e:
                        answer = 'Не найден город'
                        
                self.bot.send_message(message.chat.id, answer)

        self.bot.polling(none_stop=True, interval=0)



bt=bot_facts()

bt.main()

############################################################################
#
#   PROJECT_08 - end
#
############################################################################




