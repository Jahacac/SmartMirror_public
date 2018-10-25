
from imutils.video import VideoStream
from imutils.video import FPS
import datetime
import imutils
import time
import cv2
import numpy as np
import image

def detect_motion():

    print("[INFO] camera sensor warming up...")

    vs = VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start() # Raspberry Pi
    time.sleep(2.0)
    i = 0
    detected = 0
    crop_rectangle = (50, 50, 100, 100)

    while True:

        prev = vs.read()
        prev = imutils.resize(prev, width=600)
        prev = prev[50:100, 50:100]
        prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

        frame = vs.read()
        frame = imutils.resize(frame, width=600)

        current = frame[50:100, 50:100]
        #cv2.imshow("cropped", current)
        #cv2.waitKey(0)

        gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)

        bX = 50
        bY = 50
        bW = 50
        bH = 50

        cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),
            (255, 100, 255), 1)

        err = np.sum((prevgray.astype("float") - gray.astype("float")) ** 2)
        err /= float(prevgray.shape[0] * gray.shape[1])

        if err > 100:
            detected += 1
        text = "movements: {}".format(detected)
        cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 1)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()


if __name__ == '__main__':
    detect_motion()
