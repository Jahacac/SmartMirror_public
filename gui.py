from tkinter import *
from threading import Lock, Thread

import tkinter
import locale
import threading
import time

from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

ui_locale = ''
time_format = 24 # 12/24
date_format = "%B %d, %Y"
xlarge_text_size = 94
large_text_size = 48
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

class Gui:

    def __init__(self, value): #konstruktor, tu imamo value (face flag-kad inicijliziramo je False, poslje se mijenja sa check_face) jer poslje value koristimo u svim funkcijama pa da nebude globalna varijabla
        self.value = value
        self.lock = Lock()
        self.root = Tk() #globalne varijable koje ce gui 100% koristit i funkcijama upravljamo njima, pokusala sam da nebudu globalne al je tlaka tlaka tlaka^4 nije mi radilo
        self.clock = Label(self.root, font=("times", 50, "bold"), bg= "black", fg = "white")

        self.root.configure(background='black') #treba dodat tipka za gasenje
        #self.root.overrideredirect(True)
        #self.root.overrideredirect(False)
        self.root.attributes('-fullscreen',True) #fullscreen sam makla tek tako da vidim dal se flagovi dobro salju (gledala u ispis printera i gui)

        #time label
        self.time1 = ''
        self.timeLbl = tkinter.Label(self.root, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=tkinter.TOP, anchor=tkinter.E)
        #dan u tjednu label
        self.day_of_week1 = ''
        self.dayOWLbl = tkinter.Label(self.root, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=tkinter.TOP, anchor=tkinter.E)
        #date label
        self.date1 = ''
        self.dateLbl = tkinter.Label(self.root, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=tkinter.TOP, anchor=tkinter.E)
        #facedetection label
        self.fdetection = tkinter.Label(self.root, text=self.value, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.fdetection.pack(side=tkinter.TOP, anchor=tkinter.E)

        self.tick()

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

    def mainloop(self): #da se root mainloop ne pozove odmah
        self.root.mainloop()

