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

GUI_HAS_FACE = True

from face_detection import FaceDetection

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

def gui_check_face(has_face, clock):
    global GUI_HAS_FACE
    GUI_HAS_FACE = has_face
    if GUI_HAS_FACE:
        clock.config(text='has face')
    else:
        clock.config(text='no face')

def main():
    global GUI_HAS_FACE
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True, #ili p ili shape predictor se koriste u commandlineu, true jer je obavezno
        help="path to facial landmark predictor") #kad upisemo help u cl nam to ispise
    args = ap.parse_args()

    p = Printer(1)
    p.start()



    def tick():
        time_string = time.strftime("%H:%M:%S")
        clock.config(text=time_string)
        clock.after(200, tick)

    root = Tk()
    clock = Label(root, font=("times", 50, "bold"), bg="black", fg="white")

    temp_f = lambda has_face: gui_check_face(has_face, clock) #lambda je temporary funkcija u pythonu
    face = FaceDetection(args.shape_predictor, face_callbacks=[p.face_update, temp_f])
    face.start()

    if GUI_HAS_FACE:
        pass
    else:
        pass


    clock.grid(row=0, column=0)
    tick()

    #root.configure(background='black')
    #root.attributes('-fullscreen',True)

    root.wm_attributes("-topmost", 1)
    root.focus_set()

    root.bind("<Escape>", lambda event:root.destroy())
    root.mainloop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print("Me die now.")



