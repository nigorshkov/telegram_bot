# -*- coding: utf-8 -*-
import requests
import datetime
import lib.config

dict_condition = {
'clear': 'Ясно',
'partly-cloudy': 'Малооблачно',
'cloudy': 'Облачно с прояснениями',
'overcast': 'Пасмурно',
'partly-cloudy-and-light-rain': 'Малооблачно и небольшой дождь',
'partly-cloudy-and-rain': 'Малооблачно и дождь',
'overcast-and-rain': 'Сильный дождь',
'overcast-thunderstorms-with-rain': 'Сильный дождь, гроза',
'cloudy-and-light-rain': 'Облачно и небольшой дождь',
'overcast-and-light-rain': 'Пасмурно и небольшой дождь',
'cloudy-and-rain': 'Облачно и дождь',
'overcast-and-wet-snow': 'Пасмурно и дождь со снегом',
'partly-cloudy-and-light-snow': 'Малооблачно и небольшой снег',
'partly-cloudy-and-snow': 'Малооблачно и снег',
'overcast-and-snow': 'Пасмурно и снегопад',
'cloudy-and-light-snow': 'Облачно и небольшой снег',
'overcast-and-light-snow': 'Пасмурно и небольшой снег',
'cloudy-and-snow': 'Облачно и снег'}


def get_weater(lat, lon):
    res = requests.get('https://api.weather.yandex.ru/v1/forecast',
                       params={'lat': lat, 'lon': lon, 'lang': 'ru_RU', 'limit': '1'},
                       headers={'X-Yandex-API-Key': lib.config.weather_api})
    data = res.json()
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    now_temp = data['fact']['temp']
    now_feels_like = data['fact']['feels_like']
    now_condition = dict_condition[data['fact']['condition']]
    day_temp_min = [i for i in data['forecasts'] if i['date'] ==
                    datetime.datetime.now().strftime('%Y-%m-%d')][0]['parts']['day']['temp_min']
    day_temp_max = [i for i in data['forecasts'] if i['date'] ==
                    datetime.datetime.now().strftime('%Y-%m-%d')][0]['parts']['day']['temp_max']
    day_temp_avg = [i for i in data['forecasts'] if i['date'] ==
                    datetime.datetime.now().strftime('%Y-%m-%d')][0]['parts']['day']['temp_avg']
    day_feels_like = [i for i in data['forecasts'] if i['date'] ==
                      datetime.datetime.now().strftime('%Y-%m-%d')][0]['parts']['day']['feels_like']
    day_condition = dict_condition[[i for i in data['forecasts'] if i['date'] ==
                                    datetime.datetime.now().strftime('%Y-%m-%d')][0]['parts']['day']['condition']]

    return '*Сейчас*\nТемпература= {}\nОщущаемая температура= {}\n{}\n\n' \
           '*За день*\nМинимальная температура= {}\nМаксимальная температура= {}\n' \
           'Средняя температура={}\nОщущаемая температура= {}\n{}'\
        .format(now_temp, now_feels_like, now_condition, day_temp_min,
                day_temp_max, day_temp_avg, day_feels_like, day_condition)
