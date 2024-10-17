#from Bailes import bailes
import threading
import socket
import queue
import time
import json
from Distribuido.arquitectura import BDIAgent, Environment, Beliefs, Intentions, BDI_Actions
from Distribuido.Eleccion_de_lider import Liderazgo, role
from serverDany import recibir_mensaje_server,enviar_mensaje_server,conectar_server
from clienteDany import recibir_mensaje_cliente,enviar_mensaje_cliente,conectar_cliente
from Distribuido.Generador_de_rutinas import crea_rutina
from Bailes import bailes

def participar_en_consenso(hexapodo_1):
    print(" paso por participar_en_consenso")
    
    #       [CONSENSO]: ID        10      , status:    role.CANDIDATO  , líder:        None
    print(f"[CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")

    #communication_ready.wait()

    # Enviar estado con la estructura correcta
    state_message = {
        "type": "state",
        "data": hexapodo_1.compartir_estado().copy()
    }

    #conectar_server("hexapodo2.local",5000) #empezar a escuchar solicitudes
    conectar_cliente("hexapodo2.local",5000)
    estado_hexapodo = conectar_server("0.0.0.0",5002)
    
    #recibido = recibir_mensaje_cliente(client_sokect)
    #conectar_server("hexapodo2.local",5000) #empezar a escuchar solicitudes
    #enviar_mensaje_cliente(hexapodo_1.compartir_estado())

    #recibido = recibir_mensaje_server()
    #print (f"esto fue lo que recibi {recibido}")
    #hexapodo_2 = recibido
    #print(f"[CONSENSO]: ID {hexapodo_2.id}, status: {hexapodo_2.estado}, líder: {hexapodo_2.Lider}")

    # Esperar la confirmación de recepción
    #ack_response = get_response()
    #if ack_response and "data" in ack_response and ack_response["data"].get('ack') == "received":
    #    print("Acknowledgement received from other hexapod.")
    #else:
    #    print("No acknowledgement received.")

    
    #hexapodo_1.compartir_estado()

    # esperar a recibir los estados de los demás hexápodos
    # Lo ideal seria tener un while desde el envío de los IDs hasta que se haga el consenso
    # y todos los hexápodos sepan que tienen distinto ID
    """print(f"heiler1 [CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    print(f"recibidos {recibidos}")
    hexapodo_2_id = int(list(recibidos.keys()).copy()[0])
    print(f"heiler2 [CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    print(f"__heiler2 mio: ID {hexapodo_1.id}, otro: {hexapodo_2_id}, líder: {hexapodo_1.Lider}")
    hexapodo_1.comprobar_y_corregir_UID([hexapodo_2_id])
    print(f"heiler3 [CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    #       [CONSENSO]: ID        10      , status:    role.CANDIDATO  , líder:        (int)

    # El consenso se hace de forma automática y sin comunicarse con los demás hexápodos
    # Supongamos que el hexapodo 2 tiene el siguiente estado:
    print(f"heiler4 [CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    new_recibido = {int(key): value for key, value in recibidos.items()}
    print(f"heiler5 [CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    hexapodo_2_estado = new_recibido #recibido_____ {31: role.CANDIDATO} # {id: rol}
    print(f"heiler6 [CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    hexapodo_1.elegir_lider([hexapodo_2_estado])
    print(f"heiler7 [CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    print(f"[CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    # Para este punto, ya se hizo el consenso.
    return hexapodo_1"""
    
def generar_rutina_de_baile():
    print(" paso por funcion generar_rutina_baile")
    numero_bailes=6
    baile = crea_rutina(numero_bailes)
    #mitad = len(baile)//2
    #subrutina1=baile[:mitad]
    #subrutina2=baile[mitad:]
    #return subrutina1, subrutina2
    return baile

def partir_rutina(rutina):
    mitad = len(rutina)//2
    subrutina1=rutina[:mitad]
    subrutina2=rutina[mitad:]
    return subrutina1, subrutina2

def ejecutar_subrutina(subrurina):
    print(" paso por funcion ejecutar_subrutina")
    b=bailes()
    for baile in subrurina:
        metodo = getattr(b,baile)
        metodo()

if __name__ == '__main__':
    """b = bailes()
    
    b.baile_1()"""
    # Inicializando el agente y el entorno de la arquitectura
    h1 = BDIAgent(completions=0, energy=20000)
    hexapodo_1 = Liderazgo(k_devices=2)
    env = Environment()
    print("[INFO] Agente creado")
    print(f"[INFO] BDI_Actions.ACOMPAÑADO: {BDI_Actions.ACOMPAÑADO}")
    print(f"[INFO] h1.beliefs: {h1.beliefs.beliefs}")
    comunicación = False

    raspberrypi_name = socket.gethostname()
    if raspberrypi_name == 'hexapodo1':
        server_host = 'hexapodo2.local'
        client_name = 'hexapodo1.local'
    else:
        server_host = 'hexapodo1.local'
        client_name = 'hexapodo2.local'

    

    print (raspberrypi_name)
    print (client_name)
    print (server_host)

    comunicación = False

    

    while h1.max_completions > h1.completes and h1.max_tries > h1.tries and h1.energy > 0:
        if not h1.beliefs.beliefs[BDI_Actions.ACOMPAÑADO] and not comunicación:
            print(f"[INFO] El agente no está acompañado!")
            print(f"[COMUNICACIÓN] Buscando a alguien para balar el pasito perrón")
            comunicación = True # supongamos que se estableció la comunicación
            # Establecer conexión
            env.buddy_here = True
            print(f"[COMUNICACIÓN] Comunicación establecida exitosamente con otro agente")
        if not comunicación:
            print(f"[ERROR] No se pudo establecer la comunicación con nadie")
            print(f"[ERROR] El agente no puede bailar solo")
            exit()
        # Si el agente está acompañado, entonces participa en el consenso
        print(f"[INFO] El agente está acompañado")
        print(f"[CONSENSO] Participando en el consenso")
        hexapodo_1 = participar_en_consenso(hexapodo_1)
        hexapodo_1.estado = role.LIDER

        ##no olvidar quitar el lider hardcod.....

        #envia rutina 
        rutina = generar_rutina_de_baile()
        state_message = {
            "type": "state",
            "data": rutina
        }
        #modificar
        #send_custom_message(client_name, json.dumps(state_message))

        # Esperar respuesta
        #modificar
        #communication_ready.wait()
        #response = get_response()
        response=""
        if response:
            # Procesar el estado recibido
            if "data" in response:
                recibidos = response["data"]  # Se usa "data" en lugar de "message"
                print(f"Received state from other hexapod: {recibidos}")

                # Enviar confirmación de recepción
                ack_message = {
                    "type": "ack",
                    "data": {"ack": "received"}
                }
                #modificar
                #send_custom_message(client_name, json.dumps(ack_message))
            else:
                print("Received response does not contain 'data'.")
        else:
            print("No response received.")


        if hexapodo_1.estado == role.LIDER:
            print(f"[BAILE] Generando rutina de baile")
            #rutina = generar_rutina_de_baile()
            print(f"[BAILE] Voy con rutina {rutina}")
            subrutina1,subrutina2=partir_rutina(rutina)
            print(f"[BAILE] Rutina de baile generada")
            print(f"[BAILE] Subrutina 1 {subrutina1}")
            print(f"[BAILE] Subrutina 2 {subrutina2}")
            print(f"[BAILE] transmitiendo rutina de baile a los demás hexápodos")
            ... # Transmitir la rutina de baile a los demás hexápodos
            print(f"[BAILE] Rutina de baile transmitida exitosamente")
            # Esperar a que los demás hexápodos respondan con la confirmación de la rutina de baile
            print(f"[BAILE] Esperando confirmación de la rutina de baile")
            confirmacion_de_baile = True
            print(f"[BAILE] Confirmación de la rutina de baile recibida")
        # Escucha por rutina
        else:
            print(f"[BAILE] Esperando la rutina de baile")
            ... # Esperar a recibir la rutina de baile
            print(f"[BAILE] Voy con recibidos {recibidos}")
            subrutina1,subrutina2 = partir_rutina(recibidos)

            print(f"[BAILE] Rutina de baile recibida")
            print(f"[BAILE] Enviando confirmación de la rutina de baile")
            ... # Enviar confirmación de la rutina de baile
            print(f"[BAILE] Confirmación de la rutina de baile enviada")
            confirmacion_de_baile = True
            #subrutina1, subrutina2 = None
        if confirmacion_de_baile:
            print(f"[BAILE] Bailando subrutina 1")
            ejecutar_subrutina(subrutina1)
            print(f"[BAILE] Subrutina 1 completada, enviando confirmación a los demás hexápodos")
            ...
            print(f"[BAILE] Confirmación de la subrutina 1 enviada")
            print(f"[BAILE] Esperando confirmación de la subrutina 1 de los demás hexápodos")
            confirmacion_de_subrutina_1 = True
            if not confirmacion_de_subrutina_1:
                ... # Esperar hasta recibirla
            print(f"[BAILE] Confirmación de la subrutina 1 recibida")
            print(f"[BAILE] Bailando subrutina 2")
            ejecutar_subrutina(subrutina2)
            print(f"[BAILE] Subrutina 2 completada, enviando confirmación a los demás hexápodos")
            ...
            print(f"[BAILE] Confirmación de la subrutina 2 enviada")
            print(f"[BAILE] Esperando confirmación de la subrutina 2 de los demás hexápodos")
            confirmacion_de_subrutina_2 = True
            print(f"[BAILE] Confirmación de la subrutina 2 recibida")
            print(f"[INFO] Rutina completada")
            h1.completes += 1


                    


        rutina = "exapodo.obener_rutina()"
        
        h1.tries = 3

    """while h1.max_completions > h1.completes and h1.max_tries > h1.tries and h1.energy > 0:
        print(f"\n[INFO] Completions: {h1.completes}")
        if not BDI_Actions.ACOMPAÑADO in h1.beliefs.beliefs.keys():
            print(f"\n[ERROR] Error en las creencias del agente no sabe si está acompañado o no")
            print(f"[ERROR] Por favor revise las creencias del agente para asegurarse de que estén completas")
            exit()
        if not h1.beliefs.beliefs[BDI_Actions.ACOMPAÑADO] and not comunicación:
            print(f"[INFO] El agente no está acompañado!")
            print(f"[COMUNICACIÓN] Buscando a alguien para balar el pasito perrón")
            comunicación = True # supongamos que se estableció la comunicación
            # Establecer conexión
            env.buddy_here = True
            print(f"[COMUNICACIÓN] Comunicación establecida exitosamente con otro agente")
        if not comunicación:
            print(f"[ERROR] No se pudo establecer la comunicación con nadie")
            print(f"[ERROR] El agente no puede bailar solo")
            exit()
        rutina = "exapodo.obener_rutina()"

        h1.tries = 3"""