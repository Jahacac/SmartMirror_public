from imutils.video import VideoStream
from imutils import face_utils
import argparse #zbog parsiranja command line argumenata
import imutils
import time
import dlib
import cv2
from threading import Lock, Thread


class FaceDetection(Thread):

    def has_face(self): #funkcija koja vraća flag lica
        return self._has_face

    def set_has_face(self, value):
        old_value = self._has_face
        self._has_face = value
        if old_value != value:
            for update in self.face_callbacks: #poziva i postavlja flag lica u svim funkcijama u face_callbacks
                update(self._has_face)

    def __init__(self, shape_predictor_path, show_display=True, face_callbacks=None): #konstruktor  #nemozemo tu stavit prazno polje onda je medu svim face detection klasama dijeljeno
        Thread.__init__(self) #konstruktor od dretve

        if face_callbacks is None: #prazno polje ako nema funkcija
            face_callbacks = []

        self.shape_predictor_path = shape_predictor_path #inicijalizacija
        self.show_display = show_display
        self._has_face = False
        self.face_callbacks = face_callbacks


    def run(self): #funkcija koja se izvodi kada pokrenemo dretvu sa objekt.start()

        #inicijalizacija dlibovog face detektora i stvaranje face predictora
        print("[INFO] loading facial landmark predictor...")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.shape_predictor_path)

        #inicijalizacija video streama koj se pokrece nakon kratke pauze kako bi
        #dali vremena kamerici da se upali
        print("[INFO] camera sensor warming up...")

        vs = VideoStream(src=0).start()
        # vs = VideoStream(usePiCamera=True).start() #Raspberry Pi
        time.sleep(2.0)

        #loop frame-ova video streama
        while True:
            #uzmi frame iz video streama i promjeni mu velicinu tako da ima max sirinu
            # 400px i prebaci u grayscale
            frame = vs.read()
            frame = imutils.resize(frame, width=600)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #detektira lice u grayscale
            rects = detector(gray, 0)

            self.set_has_face(len(rects) != 0)


            #provjeri dal je lice detektirano, ako je, napisi koliko ih je
            if len(rects) > 0:
                text = "{} people found".format(len(rects))
                cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 1)

                  #loop po detekcijama lica (moze ih detektirati i vise)
                for rect in rects:
                    #izracunaj i nacrtaj kvadratic oko lica
                    (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
                    cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),
                        (255, 100, 255), 1)

                    #odredi tocke detekcije
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)

                    #loop po tockama detekcije i crtanje
                    for (i, (x, y)) in enumerate(shape):
                        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                        cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        #cleanup
        cv2.destroyAllWindows()
        vs.stop()

