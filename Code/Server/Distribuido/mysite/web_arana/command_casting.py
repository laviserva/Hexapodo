# ["ctrl-avanzar", "15"], ["ctrl-girar", "90"], ["ctrl-girar", "-90"], ["ctrl-avanzar_hasta_obstaculo"], ["sound-play"]

def gestion_comandos(comandos: list):
    comandos_out = {}


    for i, m in enumerate(comandos):

        if m == "ctrl-avanzar":
            comandos_out[i] = ctrl_avanzar(comandos[i+1])

        elif m == "ctrl-girar":
            comandos_out[i] = ctrl_girar(comandos[i+1])

        elif m == "ctrl-girar_izquierda":
            comandos_out[i] = ctrl_girar_izquierda()

        elif m == "ctrl-girar_derecha":
            comandos_out[i] = ctrl_girar_derecha()

        elif m == "ctrl-avanzar_hasta_obstaculo":
            comandos_out[i] = ctrl_avanzar_hasta_obstaculo()

        elif m == "sound-play":
            comandos_out[i] = sound_play()

        elif m == "sound-stop":
            comandos_out[i] = sound_stop()

        else:
            print(f"[Servidor]: Comando: {m} no reconocido.")
            continue

    return comandos_out

def ctrl_avanzar(distancia: str):
    return ["ctrl-avanzar", distancia]

def ctrl_girar(angulo: str):
    return ["ctrl-girar", angulo]

def ctrl_girar_izquierda():
    return ["ctrl-girar", "-90"]

def ctrl_girar_derecha():
    return ["ctrl-girar", "90"]

def ctrl_avanzar_hasta_obstaculo():
    return ["ctrl-avanzar_hasta_obstaculo"]

def sound_play():
    return ["sound-play"]

def sound_stop():
    return ["sound-stop"]