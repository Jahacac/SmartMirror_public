***********face_detection, prikaze se kamera i koliko lica je prepoznao itd.

pokrece se tako da u terminalu udes u directory u kojem se ovo sve nalazi,
utipkaj:
python face_detection.py --shape-predictor shape_predictor_5_face_landmarks.dat

za face detection nam treba taj .dat koj je ekstremno kompliciran (strojno ucenje i pizdarije)

ako terminal jede govna da ne prepoznaje cv2:
pip install opencv-python

za ostale libraries ista stvar, samo "pip install dlib" ili blabla stagod mu fali

(prije nego bilosta instaliras):
1) odi u settings i provjeri dal je enviroment namjesten na SmartMirror
2) ako je oznacen onaj zeleni kruzic tamo, ODZNACI GA
3) kad ides instalirat neki package (pip install blabla) pazi da si s terminalom u pravom enviromentu

*3) conda info --envs (prikaze sve enviroments)
    source activate SmartMirror (ude u nas enviroment)

**********jednostavni al los motion_detection

pamti previous i current frame i onda croppa 2 bw slike iz njih (rozi kvadratic)
pomocu 'err' racuna razliku izmedu te dve slike.
err == 0 znaci da su skrozz identicne. u 'if' sam stavila veci err da ne pizdi stalno nego samo kad je
velika promjena
