import cv2
import dlib
import time
from scipy.spatial import distance
from playsound import playsound
import threading
from threading import Timer, Thread, Event


conteo = 0
conteoOjosAbiertos = 0
microsuenos = 0
contadorMicrosuenos = 0
contadorPantalla = 0
contadorSeg = 0
contadorMin = 0
contadorHora = 0
currentClock = 0


def enviarSMS(message):
    print(message)


def contadorScreen():
    while True:
        global contadorSeg
        global contadorMin
        global contadorHora
        global currentClock
        time.sleep(1)
        contadorSeg += 1
        if(contadorSeg == 60):
            contadorSeg = 0
            contadorMin = +1
        if(contadorMin == 60):
            contadorSeg = 0
            contadorMin = 0
            contadorHora = +1
        if(contadorHora == 24):
            contadorSeg = 0
            contadorMin = 0
            contadorHora = 0
        currentClock = str(contadorHora)+":" + \
            str(contadorMin)+":"+str(contadorSeg)
        key = cv2.waitKey(1)
        if key == 27:
            break


def joinThread():
    playMusic.join()


def playAlert():
    playsound('alarma_de_coche_con_bocina.mp3')
    threadJoin.start()


contadorPantalla = threading.Thread(target=contadorScreen)
playMusic = threading.Thread(target=playAlert)
threadJoin = threading.Thread(target=joinThread)


def calculate_EAR(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear_aspect_ratio = (A+B)/(2.0*C)
    return ear_aspect_ratio


cap = cv2.VideoCapture(0)
hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor(
    "shape_predictor_68_face_landmarks.dat")
try:
    contadorPantalla.start()
except:
    print("manage error")
    contadorPantalla = threading.Thread(target=contadorScreen)
    contadorPantalla.start()

while True:
    start = time.time()
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = hog_face_detector(gray)
    for face in faces:

        face_landmarks = dlib_facelandmark(gray, face)
        leftEye = []
        rightEye = []

        for n in range(36, 42):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            leftEye.append((x, y))
            next_point = n+1
            if n == 41:
                next_point = 36
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)

        for n in range(42, 48):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            rightEye.append((x, y))
            next_point = n+1
            if n == 47:
                next_point = 42
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)

        left_ear = calculate_EAR(leftEye)
        right_ear = calculate_EAR(rightEye)
        cv2.putText(frame, "Microsuenos:", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (231, 1, 0), 4)
        cv2.putText(frame, str(microsuenos), (140, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (231, 1, 0), 4)
        cv2.putText(frame, "Conduccion:", (50, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (231, 1, 0), 4)
        cv2.putText(frame, str(currentClock), (140, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (231, 1, 0), 4)
        EAR = (left_ear+right_ear)/2
        EAR = round(EAR, 2)
        if(contadorMicrosuenos == 3):
            print("Microsueños: ", microsuenos)
            print("Tiempo de Conducción", currentClock)
            contadorMicrosuenos = 0

        if EAR < 0.2:
            if conteo > 30:
                if(not playMusic.is_alive()):
                    try:
                        microsuenos = microsuenos+1
                        contadorMicrosuenos += 1
                        playMusic.start()
                    except:
                        print("manage error")
                        playMusic = threading.Thread(target=playAlert)
                        playMusic.start()  # start thread
                conteo = 0
            conteo = conteo+1
            cv2.putText(frame, "Somnoliento", (10, 200),
                        cv2.FONT_ITALIC, 1, (231, 1, 0), 4)

            # print("Drowsy")
        else:
            conteoOjosAbiertos = conteoOjosAbiertos+1
            if(conteoOjosAbiertos > 30):
                conteo = 0
                conteoOjosAbiertos = 0
#        print(EAR)
#        print("conteo", conteo)
#        print("conteoOjosAbiertos", conteoOjosAbiertos)
#        print("Tiempo de ejecución", str(end - start))
        end = time.time()

    cv2.imshow("Are you Sleepy", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
