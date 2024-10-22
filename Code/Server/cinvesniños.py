import socket
from time import sleep
from bailes import bailes

class posibles_movimientos:
    ADELANTE = 'ADELANTE'
    ATRAS = 'ATRAS'
    IZQUIERDA = 'IZQUIERDA'
    DERECHA = 'DERECHA'
    DIAGONAL_ARRIBA_IZQUIERDA = 'DIAGONAL_ARRIBA_IZQUIERDA'
    DIAGONAL_ARRIBA_DERECHA = 'DIAGONAL_ARRIBA_DERECHA'
    DIAGONAL_ABAJO_IZQUIERDA = 'DIAGONAL_ABAJO_IZQUIERDA'
    DIAGONAL_ABAJO_DERECHA = 'DIAGONAL_ABAJO_DERECHA'
    GIRAR_IZQUIERDA = 'GIRAR_IZQUIERDA'
    GIRAR_DERECHA = 'GIRAR_DERECHA'
    BAILAR = 'BAILAR'

if __name__ == '__main__':
    repetir = True

    x = 0
    y = 0
    speed = 0
    angle = 0

    while repetir:

        # Tomar voz al niño
        ...

        # Traducir
        orden = ...

        # Si la orden es detente, salir del while
        if orden == 'detente':
            repetir = False
            break

        # Compara orden con comandos de posibles_movimientos
        if orden.lower() == posibles_movimientos.ADELANTE.lower():
            ...
        elif orden.lower() == posibles_movimientos.ATRAS.lower():
            ...
        elif orden.lower() == posibles_movimientos.IZQUIERDA.lower():
            ...
        elif orden.lower() == posibles_movimientos.DERECHA.lower():
            ...
        elif orden.lower() == posibles_movimientos.DIAGONAL_ARRIBA_IZQUIERDA.lower():
            ...
        elif orden.lower() == posibles_movimientos.DIAGONAL_ARRIBA_DERECHA.lower():
            ...
        elif orden.lower() == posibles_movimientos.DIAGONAL_ABAJO_IZQUIERDA.lower():
            ...
        elif orden.lower() == posibles_movimientos.DIAGONAL_ABAJO_DERECHA.lower():
            ...
        elif orden.lower() == posibles_movimientos.GIRAR_IZQUIERDA.lower():
            ...
        elif orden.lower() == posibles_movimientos.GIRAR_DERECHA.lower():
            ...
        elif orden.lower() == posibles_movimientos.BAILAR.lower():
            ...
        
        # Asignar numero de veces de ejecución a cada paso
        ...

        # Elegir comando de bailes
        