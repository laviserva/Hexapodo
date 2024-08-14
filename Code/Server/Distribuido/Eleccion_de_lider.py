import threading
import time
import random
import numpy as np
from enum import Enum, auto
from scipy.optimize import fsolve

class role(Enum):
    # Estados del robot
    SEGUIDOR = auto()
    CANDIDATO = auto()
    LIDER = auto()

class Liderazgo:
    """Se utiliza el algoritmo de Bully"""
    def __init__(self, k_devices, P=0.95):
        # Parámetros principales
        self.k = k_devices
        self.P = P

        self.id = None
        self.available_IDs = None
        self.select_id()
        self.id_historial = [self.id]

        self.estado = role.CANDIDATO
        self.lider_args = None
        self.Lider = None
        self.soy_lider = False

        # Parámetros de tiempo para heartbeat
        self.timeout = 0.3 # threshould
        self.time_wait = 0 # tiempo de respuesta del líder
        self.time_send_heartbeat = 1
    
    def comprobar_y_corregir_UID(self, ids: list[int]) -> bool:
        """
        Esta funcion comprueba si el id está en la lista de ids de otros dispositivos (sin incluir el propio),
        si es así se cambia el id seleccionando otro al azar, esto es así debido a que, la función de selección
        del ID puede estar en colisión, la funcion que genera los ID está hecho para que la posibilidad de colisión
        sea menor al 5%. Si se detecta una colisión, se cambia el ID y se retorna True, en caso contrario se retorna
        False.

        Si se quiere que la posibilidad de choque sea menor, se puede cambiar el valor de P en la clase Liderazgo en el
        inicializador.

        Cuando entra la lista de IDs, se actualiza el número de dispositivos disponibles para seleccionar un ID para 
        minimizar las posibilidades de colisión en el futuro con el parámetro deseado P.

        Args:
            ids (list[int]): Lista de numeros enteros que contiene los IDs de otros dispositivos

        Returns:
            bool: Retorna True si se cambió el ID, en caso contrario False
        """
        actualizo = True
        while self.id in ids:
            actualizo = False
            self.k = len(ids) + 1
            self.id, self.available_IDs = self.select_id()
            self.id = random.randint(0, self.available_IDs)
        return actualizo

    def select_id(self):
        def equation(k, P, n):
            left_side = np.log(P**2) + 2 * n
            right_side = (2 * (k - n) + 1) * np.log(k / (k - n))
            return left_side - right_side

        # Iterar sobre los valores de P
        if self.k <= 1:
            return 1
        initial_guess = self.k + 1
        k_solution = fsolve(equation, initial_guess, args=(self.P, self.k))[0]
        k_solution = int(np.ceil(k_solution))

        self.id = random.randint(0, k_solution)
        self.available_IDs = k_solution

        return self.id, self.available_IDs
    
    def compartir_estado(self) -> dict[role]:
        """
        Función que se encarga de compartir el estado del dispositivo con el resto de dispositivos, para elegir lider
        """
        return {self.id: self.estado}

    def elegir_lider(self, estado: dict[role]):
        """
        Hace que el dispositivo actual sea candidato a líder, si no hay un líder actualmente siguiendo el algoritmo de Bully, 
        establece un conjunto de pasos a seguir

        1. enviar_mensaje: Envía mensaje de elección al resto de robots
        2. recepcion_de_respuestas: Los robots que reciben el mensaje de Elección responden con un mensaje de OK y sus UIDs
        3. eleccion_de_lider: Se elige el líder con el UID más alto

        Args:
            estado (dir[role]): Diccionario con los estados de los dispositivos
            {id: estado}
        """
        if not estado:
            print("[ERROR] No hay dispositivos disponibles")
            exit()

        self.lider_args = estado

        estado_id = []
        estado_rol = []

        for item in estado:
            for key, value in item.items():
                estado_id.append(key)
                estado_rol.append(value)
            
        lider = max(estado_id)
        if self.id > lider:
            lider = self.id
            self.soy_lider = True
        if self.estado == role.CANDIDATO and self.Lider is None:
            if lider == self.id:
                self.estado = role.LIDER
            else:
                self.estado = role.SEGUIDOR
        else:
            print(f"[INFO] El dispositivo lider es: {self.id} y el estado actual es: {self.estado}")
        self.time_wait = time.time()
        self.Lider = lider
        return lider
    
    def enviar_heartbit(self):
        """
        Función que se encarga de enviar un mensaje de heartbeat al resto de dispositivos
        """
        # al lider
        if self.estado == role.LIDER:
            def enviar():
                while True:
                    print(f"[HEARTBEAT] Líder {self.id} enviando heartbeat...")
                    time.sleep(self.time_send_heartbeat)  # Enviar cada 5 segundos
            
            heartbeat_thread = threading.Thread(target=enviar)
            heartbeat_thread.daemon = True
            heartbeat_thread.start()

    def recibir_heartbit(self, mensaje_lider: str) -> bool:
        """
        Función que se encarga de recibir un mensaje de heartbeat del líder, si no hay respuesta en un tiempo determinado
        se elige un nuevo líder.

        Los mensajes de heartbeat son enviados por el líder cada cierto tiempo para comprobar si los dispositivos están
        activos.

        Args:
            mensaje_lider (str): Mensaje de heartbeat del líder
        """
        still_leader = True
        if mensaje_lider != "heartbeat":
            return still_leader
        
        if time.time() - self.time_wait > self.timeout:
            still_leader = False
            print(f"[INFO] El líder {self.Lider} no responde, se elige un nuevo líder")
            self.estado = role.CANDIDATO
            self.Lider = None
            self.soy_lider = None

        return still_leader
    


if __name__ == "__main__":
    k = 3
    robot_1 = Liderazgo(k_devices=k)
    robot_2 = Liderazgo(k_devices=k)
    robot_3 = Liderazgo(k_devices=k)

    # supongamos una colisión
    robot_1.id = 1
    robot_2.id = 1

    print(f"Robot 1: {robot_1.id}, status: {robot_1.estado}, líder: {robot_1.Lider}")
    print(f"Robot 2: {robot_2.id}, status: {robot_2.estado}, líder: {robot_2.Lider}")
    print(f"Robot 3: {robot_3.id}, status: {robot_3.estado}, líder: {robot_3.Lider}")
    print()

    robot_1.comprobar_y_corregir_UID([robot_2.id, robot_3.id])
    robot_2.comprobar_y_corregir_UID([robot_1.id, robot_3.id])
    robot_3.comprobar_y_corregir_UID([robot_1.id, robot_2.id])

    print(f"Robot 1: {robot_1.id}, status: {robot_1.estado}, líder: {robot_1.Lider}")
    print(f"Robot 2: {robot_2.id}, status: {robot_2.estado}, líder: {robot_2.Lider}")
    print(f"Robot 3: {robot_3.id}, status: {robot_3.estado}, líder: {robot_3.Lider}")
    print()

    robot_1.elegir_lider([robot_2.compartir_estado(), robot_3.compartir_estado()])
    robot_2.elegir_lider([robot_1.compartir_estado(), robot_3.compartir_estado()])
    robot_3.elegir_lider([robot_1.compartir_estado(), robot_2.compartir_estado()])

    print(f"Robot 1: {robot_1.id}, status: {robot_1.estado}, líder: {robot_1.Lider}")
    print(f"Robot 2: {robot_2.id}, status: {robot_2.estado}, líder: {robot_2.Lider}")
    print(f"Robot 3: {robot_3.id}, status: {robot_3.estado}, líder: {robot_3.Lider}")
    print()

    lider = [robot_1.Lider, robot_2.Lider, robot_3.Lider]
    lider = max(lider)
    # forzar lider
    robot_1.estado = role.LIDER
    robot_1.Lider = lider
    robot_2.estado = role.SEGUIDOR
    robot_2.Lider = lider
    robot_3.estado = role.SEGUIDOR
    robot_3.Lider = lider

    # forcemos a que el timeout se cumpla
    still_leader_r1 = robot_1.recibir_heartbit("heartbeat")
    still_leader_r2 = robot_2.recibir_heartbit("heartbeat")
    still_leader_r3 = robot_3.recibir_heartbit("heartbeat")
    
    stills = [(still_leader_r1, robot_1),
              (still_leader_r2, robot_2),
              (still_leader_r3, robot_3)]
    
    if not still_leader_r1:
        robot_1.elegir_lider([robot_2.compartir_estado(), robot_3.compartir_estado()])
    if not still_leader_r2:
        robot_2.elegir_lider([robot_1.compartir_estado(), robot_3.compartir_estado()])
    if not still_leader_r2:
        robot_3.elegir_lider([robot_1.compartir_estado(), robot_2.compartir_estado()])

    time.sleep(1)

    robot_1.select_id()
    robot_2.select_id()
    robot_3.select_id()
    print()

    # forcemos a que el timeout se cumpla
    still_leader_r1 = robot_1.recibir_heartbit("heartbeat")
    still_leader_r2 = robot_2.recibir_heartbit("heartbeat")
    still_leader_r3 = robot_3.recibir_heartbit("heartbeat")

    if not still_leader_r1:
        robot_1.elegir_lider([robot_2.compartir_estado(), robot_3.compartir_estado()])
    if not still_leader_r2:
        robot_2.elegir_lider([robot_1.compartir_estado(), robot_3.compartir_estado()])
    if not still_leader_r2:
        robot_3.elegir_lider([robot_1.compartir_estado(), robot_2.compartir_estado()])

    print()

    print(f"Robot 1: {robot_1.id}, status: {robot_1.estado}, líder: {robot_1.Lider}")
    print(f"Robot 2: {robot_2.id}, status: {robot_2.estado}, líder: {robot_2.Lider}")
    print(f"Robot 3: {robot_3.id}, status: {robot_3.estado}, líder: {robot_3.Lider}")