#!/usr/bin/env python

import gi
gi.require_version('Notify', '0.7')
import json
import requests
from gi.repository import Notify


sprut_json = requests.get("http://tuxbox/sprut/sprut.json")
weather_data = json.loads(sprut_json.content)


def get_wind():
    if weather_data['MC_WindDirection_Long_ua'] == "Штиль":
        wind = "<b>Вітер:</b> " + weather_data['MC_WindDirection_Long_ua']
    else:
        wind = "<b>Вітер:</b> " \
                + weather_data['MC_WindDirection_Long_ua'] \
                + " (" + str(weather_data['M_DIRAVG2M']) + "°)"
    return str(wind)


def send_notification(title, text, full_path_to_icon=""):
    Notify.init("Weather")
    n = Notify.Notification.new(title, text, full_path_to_icon)
    n.show()


txt = [
        "Вараш  ",
        "<b>Температура:</b> ",
        "<b>Вологість:</b> ",
        "<b>Швидкість вітру:</b> ",
        "<b>Видимість:</b> ",
        "<b>Тип погоди:</b> ",
        "<b>Інтенсивність опадів:</b> "
]

last_query = weather_data['LastQueryStr']

send_notification(
    txt[0] + last_query + "\n",
    txt[1] + "%s °C\n" % weather_data['M_TA_1M_AVG'] +
    txt[2] + "%s %%\n" % weather_data['M_RH_1M_AVG'] +
    get_wind() + "\n" +
    txt[3] + "%s м/c" % weather_data['M_SPDAVG2M'] + "\n" +
    txt[4] + "%s м\n" % weather_data['M_VIS_1'] +
    txt[5] + "%s\n" % weather_data['MC_TypeWeather_Short_ua'] +
    txt[6] + "%s мм/год" % weather_data['M_WATER_1H'], 'gnome-weather')
Notify.uninit()
