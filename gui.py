# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow

import tkinter
import locale
import threading
import time

from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 24 # 12 or 24
date_format = "%B %d, %Y" # check python doc for strftime() for options
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock(tkinter.Frame):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = tkinter.Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=tkinter.TOP, anchor=tkinter.E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = tkinter.Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=tkinter.TOP, anchor=tkinter.E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = tkinter.Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=tkinter.TOP, anchor=tkinter.E)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            self.timeLbl.after(200, self.tick)

class Calendar(tkinter.Frame):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, bg='black')
        self.title = 'Calendar Events'
        self.calendarLbl = tkinter.Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.calendarLbl.pack(side=tkinter.TOP, anchor=tkinter.E)
        self.calendarEventContainer = tkinter.Frame(self, bg='black')
        self.calendarEventContainer.pack(side=tkinter.TOP, anchor=tkinter.E)
        self.get_events()

    def get_events(self):
        #TODO: implement this method
        # reference https://developers.google.com/google-apps/calendar/quickstart/python

        # remove all children
        for widget in self.calendarEventContainer.winfo_children():
            widget.destroy()

        calendar_event = CalendarEvent(self.calendarEventContainer)
        calendar_event.pack(side=tkinter.TOP, anchor=tkinter.E)
        pass


class CalendarEvent(tkinter.Frame):
    def __init__(self, parent, event_name="Event 1"):
        tkinter.Frame.__init__(self, parent, bg='black')
        self.eventName = event_name
        self.eventNameLbl = tkinter.Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=tkinter.TOP, anchor=tkinter.E)


class FullscreenWindow:

    def __init__(self):
        self.tk = tkinter.Tk()
        self.tk.configure(background='black')
        self.topFrame = tkinter.Frame(self.tk, background ='black')
        self.bottomFrame = tkinter.Frame(self.tk, background ='black')
        self.topFrame.pack(side = tkinter.TOP, fill=tkinter.BOTH, expand = tkinter.YES)
        self.bottomFrame.pack(side = tkinter.BOTTOM, fill=tkinter.BOTH, expand = tkinter.YES)
        self.tk.overrideredirect(True)
        self.tk.overrideredirect(False)
        self.tk.attributes('-fullscreen',True)
        self.tk.wm_attributes("-topmost", 1)
        self.tk.focus_set()
        self.tk.bind("<Escape>", lambda event:self.tk.destroy())
        self.state = False
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=tkinter.RIGHT, anchor=tkinter.N, padx=100, pady=60)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.after(10000, w.tk.destroy)
    w.tk.mainloop()

"""
from tkinter import *
import time

def tick():
    time_string = time.strftime("%H:%M:%S")
    clock.config(text=time_string)
    clock.after(200, tick)

root = Tk()
clock = Label(root, font=("times", 50, "bold"), bg= "black", fg = "white")
clock.grid(row=0, column=0)
tick()

root.configure(background='black')
root.overrideredirect(True)
root.overrideredirect(False)
root.attributes('-fullscreen',True)

root.wm_attributes("-topmost", 1)
root.focus_set()

root.bind("<Escape>", lambda event:root.destroy())
root.after(10000, root.destroy)

root.mainloop()
"""

"""
Ako se pise ovako kod^ nemoze se poslje importat u mainu i izvrsit kao zasebna dretva jer kad 
radis import se sve izvrsi i u ovom slucaju, otic ce u mainloop i sve sjebat.

Ovako treba gui pisat(u main.py):

def main():
    blabla sranja s ostalim dretvama
    blablabla gui kod

if __name__ == '__main__':
    main()
    
GUI ce bit glavna (prva) dretva jer ako se stavi u neku drugu Tkinter zna zafrkavat i bacat errore. 
Sve ostalo ce bit u drugim dretvama, pokrenite main.py i proucite.

"""
