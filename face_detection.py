from imutils.video import VideoStream
from imutils import face_utils
import argparse #zbog parsiranja command line argumenata
import imutils
import time
import dlib
import cv2
from threading import Lock, Thread


class FaceDetection(Thread):
    #uvijek moras self pisat, self je ko "this" u javi

    def has_face(self):
        return self._has_face

    def set_has_face(self, value):
        old_value = self._has_face
        self._has_face = value
        if old_value != value:
            for update in self.face_callbacks:
                update(self._has_face)

    def __init__(self, shape_predictor_path, show_display=True, face_callbacks=None): #nemozemo tu stavit prazno polje onda je medu svim face detection klasama dijeljeno
        Thread.__init__(self) #konstruktor od dretve

        if face_callbacks is None:
            face_callbacks = []

        self.shape_predictor_path = shape_predictor_path
        self.show_display = show_display
        self._has_face = False
        self.face_callbacks = face_callbacks


    def run(self):

        # initialize dlib's face detector (HOG-based) and then create the
        # facial landmark predictor
        print("[INFO] loading facial landmark predictor...")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.shape_predictor_path)

        # initialize the video stream and sleep for a bit, allowing the
        # camera sensor to warm up
        print("[INFO] camera sensor warming up...")

        vs = VideoStream(src=0).start()
        # vs = VideoStream(usePiCamera=True).start() # Raspberry Pi
        time.sleep(2.0)

        # loop over the frames from the video stream
        while True:
            # grab the frame from the threaded video stream, resize it to
            # have a maximum width of 400 pixels, and convert it to
            # grayscale
            frame = vs.read()
            frame = imutils.resize(frame, width=600)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # detect faces in the grayscale frame
            rects = detector(gray, 0)

            self.set_has_face(len(rects) != 0)


            # check to see if a face was detected, and if so, draw the total
            # number of faces on the frame
            if len(rects) > 0:
                text = "{} people found".format(len(rects))
                cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 1)

                  # loop over the face detections


                for rect in rects:
                    # compute the bounding box of the face and draw it on the
                    # frame
                    (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
                    cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),
                        (255, 100, 255), 1)

                    # determine the facial landmarks for the face region, then
                    # convert the facial landmark (x, y)-coordinates to a NumPy
                    # array
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)

                    # loop over the (x, y)-coordinates for the facial landmarks
                    # and draw each of them
                    for (i, (x, y)) in enumerate(shape):
                        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                        cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            # show the frame
            if self.show_display:
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()

