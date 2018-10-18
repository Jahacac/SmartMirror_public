napravila sam novi file face_detection, prikaze se kamera i koliko lica je prepoznao itd.

pokrece se tako da u terminalu udes u directory u kojem se ovo sve nalazi,
utipkaj:
python face_detection.py --shape-predictor shape_predictor_5_face_landmarks.dat

za face detection nam treba taj .dat koj je ekstremno kompliciran (strojno ucenje i pizdarije)

ako terminal jede govna da ne prepoznaje cv2:
pip install opencv-python

za ostale libraries ista stvar, samo "pip install dlib" ili blabla stagod mu fali


