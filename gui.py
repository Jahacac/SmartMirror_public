from tkinter import *
from threading import Lock, Thread

import tkinter
import locale
import threading
import time
import requests
import json
import traceback
import feedparser

from PIL import Image, ImageTk
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

ui_locale = ''
time_format = 24 # 12/24
date_format = "%B %d, %Y"
weather_api_token = '60da1605a073d3b86186ab70ccfd9f79' #darksky api key
#https://api.darksky.net/forecast/60da1605a073d3b86186ab70ccfd9f79/37.8267,-122.4233
weather_lang = 'hr'
weather_unit = 'auto'
latitude = '45.327065' # Rijeka, Croatia
longitude = '14.442176'
xlarge_text_size = 94
large_text_size = 58
medium_text_size = 28
small_text_size = 18

@contextmanager
def setlocale(name):
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

#postavimo ikonicu ovisno o vremenu
icon_lookup = {
    'clear-day': "assets/Sun.png",
    'wind': "assets/Wind.png",
    'cloudy': "assets/Cloud.png",
    'partly-cloudy-day': "assets/PartlySunny.png",
    'rain': "assets/Rain.png",
    'snow': "assets/Snow.png",
    'snow-thin': "assets/Snow.png",
    'fog': "assets/Haze.png",
    'clear-night': "assets/Moon.png",
    'partly-cloudy-night': "assets/PartlyMoon.png",
    'thunderstorm': "assets/Storm.png",
    'tornado': "assests/Tornado.png",
    'hail': "assests/Hail.png"
}

class Gui:

    def __init__(self, value): #konstruktor, tu imamo value (face flag-kad inicijliziramo je False, poslje se mijenja sa check_face) jer poslje value koristimo u svim funkcijama pa da nebude globalna varijabla
        self.value = value
        self.lock = Lock()

        #prvo napravimo root koji nam je cijela 'površina' za gui
        self.root = Tk() #globalne varijable koje ce gui 100% koristit i funkcijama upravljamo njima, pokusala sam da nebudu globalne al je tlaka tlaka tlaka^4 nije mi radilo
        self.root.configure(background='black')
        self.root.attributes('-fullscreen',True)

        #definiramo topFrame unutar kojeg cemo imati 2 Framea- time i weather(mora se ovako da budu u istom redu)
        self.topFrame = Frame(self.root, width=1350, height=50)
        self.topFrame.pack(side=TOP, fill=X, expand=1, anchor=N)
        self.topFrame.configure(background='black')

        #timeFrame - lijevo
        self.timeFrame = Frame(self.topFrame)
        self.timeFrame.pack(side=RIGHT, anchor=NE)
        self.timeFrame.configure(background='black')

        #LABELE za timeFrame - vrijeme, datum lala:
        #time label
        self.time1 = ''
        self.timeLbl = tkinter.Label(self.timeFrame, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=tkinter.TOP, anchor=tkinter.NE)
        #dan u tjednu label
        self.day_of_week1 = ''
        self.dayOWLbl = tkinter.Label(self.timeFrame, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=tkinter.TOP, anchor=tkinter.E)
        #date label
        self.date1 = ''
        self.dateLbl = tkinter.Label(self.timeFrame, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=tkinter.TOP, anchor=tkinter.E)
        #facedetection label
        self.fdetection = tkinter.Label(self.timeFrame, text=self.value, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.fdetection.pack(side=tkinter.TOP, anchor=tkinter.E)

        self.tick()

        #weatherFrame - desno - ista priča
        self.weatherFrame = Frame(self.topFrame, width=100, height=50)
        self.weatherFrame.pack(side=LEFT)
        self.weatherFrame.configure(background='black')

        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self.weatherFrame, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=NW)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=NW)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=NW, padx=20)
        self.currentlyLbl = Label(self.weatherFrame, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=NW)
        self.forecastLbl = Label(self.weatherFrame, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.forecastLbl.pack(side=TOP, anchor=NW)
        self.locationLbl = Label(self.weatherFrame, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=NW)

        self.get_weather()

        self.root.wm_attributes("-topmost", 1)
        self.root.focus_set()

        self.root.bind("<Escape>", lambda event: self.root.destroy())
        #self.root.after(10000, self.root.destroy)


    def check_face(self, has_face): #ovu funkciju saljemo poslje u facedetection pomocu face_callbacka i hvatamo flag za lice
        self.value = has_face #postavljamo novu vrijednost value-a

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #12h format
            else:
                time2 = time.strftime('%H:%M') #24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            #ako se je promijenio datum i/ili vrijeme
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
        #mijenjamo vrijednost labela za facedetection True/False
        self.fdetection['text'] = str(self.value)
        self.timeLbl.after(200, self.tick)

    def get_weather(self):
        try:
            location2 = ""
            weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]

            icon_id = weather_obj['currently']['icon']
            icon2 = None

            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                self.iconLbl.config(image='')

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get weather." % e)

        self.root.after(600000, self.get_weather)

    def mainloop(self): #da se root mainloop ne pozove odmah
        self.root.mainloop()

