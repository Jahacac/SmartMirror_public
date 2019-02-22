from threading import Lock, Thread
import time
import threading

from imutils.video import VideoStream
from imutils import face_utils
import argparse #zbog parsiranja command line argumenata
import imutils
import time
import dlib
import cv2

from tkinter import *
import time

GUI_HAS_FACE = False

from face_detection import FaceDetection
from gui import Gui

class Printer(Thread): #sluzi kao demo da vidimo sta se dogada u pozadini (s printanjem)
    #za dretve u ovom slucaju koristimo klase; napravimo klasu, njen konstruktor (koj nije obavezan)
    def __init__(self, value):
        Thread.__init__(self)
        self._value = value
        self.lock = Lock()

    def run(self):
        while True:
            with self.lock: #dvije stvari nemogu istovremeno vrtit taj blok koda
                print("PRINTER BLOCK")
                print("#" * 20)
                print("1) ", self._value)
                time.sleep(1)
                print("2) ", self._value)
                print("#" * 20)
            time.sleep(2)

    def face_update(self, has_face):
        with self.lock:
            self._value = has_face


def gui_check_face(has_face):
    global GUI_HAS_FACE
    GUI_HAS_FACE = has_face


def main():
    global GUI_HAS_FACE
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True, #ili p ili shape predictor se koriste u commandlineu, true jer je obavezno
        help="path to facial landmark predictor") #kad upisemo help u cl nam to ispise
    args = ap.parse_args()

    p = Printer(False) #konstruktor za printer + salje se pocetna vrijednost flag-a za lice
    p.start()

    gui = Gui(False) #konstruktor za gui + salje se pocetna vrijednost flag-a za lice
    #gui.start()

    face = FaceDetection(args.shape_predictor, face_callbacks=[p.face_update, gui.check_face]) #konstruktor za facedetection + salje flagove za lice u navedene funkcije (face_update, check_face)
    face.start()


    gui.mainloop() #uvijek mora bit na kraju


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print("Me die now.")



