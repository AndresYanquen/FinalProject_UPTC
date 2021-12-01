import time

contadorSeg = 0
contadorMin = 0
contadorHora = 0


def contadorScreen():
    global contadorSeg
    global contadorMin
    global contadorHora
    time.sleep(1)
    contadorSeg += 1
    if(contadorSeg == 60):
        contadorSeg = 0
        contadorMin = +1
    if(contadorMin == 60):
        contadorMin = 0
        contadorHora = +1
    if(contadorHora == 24):
        contadorSeg = 0
        contadorMin = 0
        contadorHora = 0
    print(str(contadorHora)+":"+str(contadorMin)+":"+str(contadorSeg))


while True:
    contadorScreen()
