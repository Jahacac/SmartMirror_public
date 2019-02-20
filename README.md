POKRETANJE NA WINDOSIMA
-----------------------
1. U Pycharmu otići na File->Settings->Project:SmartMirror->Project Interpreter
u Project Interpreter bi moralo pisati Python 3.6(SmartMirror) C:\Users\Korisnik\Anaconda3\envs\SmartMirror\python.exe
ako ne piše na ikonicu settings pa Conda Enviroment i napraviti novi.
2.Kad to završiš vratit se na Project Interpreter i kliknuti zeleni kružić Conde. To znači da će Pycharm koristiti pakete koje smo instalirali preko Conde
3. [Provjera] Otvoriti Anaconda navigator i sa strane kliknut na Enviroments i Smart Mirror bi trebao biti tamo ako nije jebiga
4. Sad treba ući u Anaconda promt i upisati activate SmartMirror (sad smo u njegovom env)
5. Otići u folder od SmartMirrora
6. napisati naredbu koja će instalirati sve iz env.txt (ima u conda cheate shitu)
7.that's it
-------------------------------
Kodovi se mogu pokretati ili iz pycharama ili ako trebaju argumente kao ivanin onda u conda promtu
npr.
activate SmartMirror
cd cd do SmartMirror
python hello.py

conda list -e > env.txt #Save all the info about packages to your folder

Naredba za instalirat sve iz env.txt:
for /f %i in (env.txt) do conda install --yes %i

POKRETANJE NA LINUXU
-----------------------
face_detection, prikaze se kamera i koliko lica je prepoznao itd.

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
