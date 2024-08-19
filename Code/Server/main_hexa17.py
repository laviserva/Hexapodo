import socket
from Bailes import bailes
from datetime import datetime

from HexapodoComunicator import HexapodoComunicator
from Distribuido.Generador_de_rutinas import crea_rutina
from Distribuido.Eleccion_de_lider import Liderazgo, role
from Distribuido.arquitectura import BDIAgent, Environment, Beliefs, Intentions, BDI_Actions

def participar_en_consenso(hexapodo_1):
    #       [CONSENSO]: ID        10      , status:    role.CANDIDATO  , líder:        None
    print(f"[CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")

    #communication_ready.wait()

    # Enviar estado con la estructura correcta
    custom_message = {
        "data": hexapodo_1.compartir_estado(),
        "hotra": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    }
    response = communicator.exchange_data(custom_message)
    print(f"[CONSENSO] respuesta: {response}")

    #send_custom_message(client_name, json.dumps(state_message))

    # Esperar respuesta

    if response:
        # Procesar el estado recibido
        if "data" in response:
            recibidos = response["data"]  # Se usa "data" en lugar de "message"
            print(f"[CONSENSO] Recibido del otro hexápodo: {recibidos} hora: {response['hotra']}")

        else:
            print("La respuesta no tiene 'data'.")
    else:
        print("No se recibió respuesta.")

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
    print(f"[CONSENSO] ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    hexapodo_2_id = int(list(recibidos.keys())[0])
    print(f"[CONSENSO] ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    print(f"[CONSENSO] ID {hexapodo_1.id}, otro ID: {hexapodo_2_id}, líder: {hexapodo_1.Lider}")
    hexapodo_1.comprobar_y_corregir_UID([hexapodo_2_id])
    #       [CONSENSO]: ID        10      , status:    role.CANDIDATO  , líder:        (int)

    # El consenso se hace de forma automática y sin comunicarse con los demás hexápodos
    # Supongamos que el hexapodo 2 tiene el siguiente estado:
    new_recibido = {int(key): value for key, value in recibidos.items()}
    hexapodo_2_estado = new_recibido #recibido_____ {31: role.CANDIDATO} # {id: rol}
    hexapodo_1.elegir_lider([hexapodo_2_estado])
    print(f"[CONSENSO] Lider elegido!")
    print(f"[CONSENSO] ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    # Para este punto, ya se hizo el consenso.
    return hexapodo_1
    
def generar_rutina_de_baile():
    numero_bailes=6
    print(f"[BAILE] Se realizarán {numero_bailes} bailes")
    baile = crea_rutina(numero_bailes)
    print(f"[BAILE] Rutina de baile generada:\n\t\t{baile}")
    return baile

def partir_rutina(rutina):
    mitad = len(rutina)//2
    subrutina1=rutina[:mitad]
    subrutina2=rutina[mitad:]
    return subrutina1, subrutina2

def ejecutar_subrutinas(rutinas):
    print(f"[BAILE] Preparando Baile\n\n")
    b=bailes()
    print(f"[BAILE] Motores listos para el baile")
    for b, baile in enumerate(rutinas):
        metodo = getattr(b,baile)
        print(f"[BAILE] Bailando subrutina {b+1}")
        metodo()
        print(f"[BAILE] Subrutina {b+1} terminada con éxito, enviando confirmación")
        state_message = {
            "data": "ok termine baile",
        }
        response = communicator.exchange_data(state_message)
        print(f"[BAILE] Confirmación de la subrutina {b+1} enviada")
        print()
    print("-"*50)
    print(f"[BAILE] Bailes terminados con éxito")
    print("-"*50)
    print()



def buscar_compañero(HexapodoComunicator, client_name, server_host):
    try:
        print(f"[INFO] El agente no está acompañado!")
        print(f"[COMUNICACIÓN] Buscando a alguien para bailar")
        communicator = HexapodoComunicator(client_name, server_host)
        print(f"[COMUNICACIÓN] Comunicación establecida exitosamente con otro agente")
    except Exception as e:
        print(f"[ERROR] No se pudo establecer la comunicación con nadie")
        print(f"[ERROR] El agente no puede bailar solo")
        print(f"[ERROR] {e}")
        exit()
    return communicator

def consenso(hexapodo_1):
    print(f"[INFO] El agente está acompañado")
    print(f"[CONSENSO] Participando en el consenso")
    hexapodo_1 = participar_en_consenso(hexapodo_1)
    print(f"[CONSENSO] Generando rutina de baile")
    rutina = generar_rutina_de_baile()
    state_message = {
    "data": rutina,
    "hora": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    print(f"[CONSENSO] Comenzando el intercambio de rutinas")
    response = communicator.exchange_data(state_message)
    print(f"[CONSENSO] Rutina intercambiada exitosamente")

    if response:
        # Procesar el estado recibido
        if "data" in response:
            recibidos = response["data"]
            print(f"[CONSENSO] Recibido del otro hexápodo: {recibidos}")
            return hexapodo_1, rutina, recibidos
        else:
            print("[CONSENSO] La respuesta recibida no contiene 'data'.")
            return hexapodo_1, rutina, None
    else:
        print("[CONSENSO] No hubo respuesta.")
    return hexapodo_1, rutina, None

if __name__ == '__main__':
    # Inicializando el agente y el entorno de la arquitectura
    h1 = BDIAgent(completions=0, energy=20000)
    env = Environment()
    h1.bdi_cycle(env)
    print(h1.intentions)
    intenciones = h1.intentions.intentions
    hexapodo_1 = Liderazgo(k_devices=2)
    print("[INFO] Agente creado")
    print(f"[BDI] BDI_Actions.ACOMPAÑADO: {BDI_Actions.ACOMPAÑADO}")
    print(f"[BDI] Creencias: {h1.beliefs.beliefs}")
    print(f"[BDI] Deseos: {h1.desires.desires}")
    print(f"[BDI] Intenciones: {h1.intentions.intentions}")
    comunicación = False
    raspberrypi_name = socket.gethostname()
    if raspberrypi_name == 'hexapodo1':
        server_host = 'hexapodo2.local'
        client_name = 'hexapodo1.local'
    elif raspberrypi_name == 'hexapodo2':
        server_host = 'hexapodo1.local'
        client_name = 'hexapodo2.local'
    communicator = HexapodoComunicator(client_name, server_host)
    rutina = None
    
    while BDI_Actions.ABORTAR not in intenciones:
        print(intenciones)
        if BDI_Actions.BUSCAR_COMP in intenciones:
            communicator = buscar_compañero(HexapodoComunicator, client_name, server_host)
            env.buddy_here = True
        if BDI_Actions.ESTABLECER_CONSENSO in intenciones:
            hexapodo_1, rutina, recibidos = consenso(hexapodo_1)
        
        if BDI_Actions.EJECUTAR_SUB1 in intenciones or BDI_Actions.EJECUTAR_SUB2 in intenciones:
            if not rutina:
                raise Exception("[BAILE] No se ha recibido la rutina de baile")
            
            print(f"[BAILE] Bailando subrutina 1")
            ejecutar_subrutinas(rutina)
            h1.completes += 1
        h1.bdi_cycle(env)