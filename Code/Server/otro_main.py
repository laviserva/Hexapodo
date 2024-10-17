import socket
import json
import asyncio
from Distribuido.arquitectura import BDIAgent, Environment, Beliefs, Intentions, BDI_Actions
from Distribuido.Eleccion_de_lider import Liderazgo, role

from Distribuido.Generador_de_rutinas import crea_rutina
from Bailes import bailes


SERVER_SEND_PORT = 65432
SERVER_RECEIVE_PORT = 65433
send_queue = asyncio.Queue()
response_queue = asyncio.Queue()

communication_ready = asyncio.Event()

# Función para crear un socket
def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Función para enviar datos en formato JSON a través de un socket
def send_json(sock, data):
    message = json.dumps(data).encode('utf-8')
    sock.sendall(message)

# Función para recibir datos en formato JSON a través de un socket
def receive_json(sock):
    response = sock.recv(4096)  # Tamaño del buffer ajustable
    return json.loads(response.decode('utf-8'))

# Función de autenticación básica
def authenticate(sock):
    auth_message = {"auth": "my_secret_key"}  # Ejemplo simple
    send_json(sock, auth_message)
    response = receive_json(sock)
    return response.get("status") == "ok"

# Tarea asincrónica que maneja la conexión del cliente
async def client_task_with_ready(client_name, server_host, port, mode, message_queue, response_queue):
    print(" paso por funcion client_thread_with_ready")
    client_socket = None
    attempts = 0
    max_attempts = 20  # Máximo de reintentos

    while attempts < max_attempts:
        try:
            print(f"Trying to connect {client_name} to {server_host}:{port}...")
            client_socket = create_socket()
            await asyncio.get_event_loop().run_in_executor(None, client_socket.connect, (server_host, port))
            client_socket.settimeout(None)
            print(f"{client_name} connected to server at {server_host}:{port} for {mode}")

            if not authenticate(client_socket):
                print("Authentication with server failed. Retrying...")
                client_socket.close()
                await asyncio.sleep(0.5)
                attempts += 1
                continue

            communication_ready.set()

            if mode == "sending":
                while True:
                    if not message_queue.empty():
                        message = await message_queue.get()
                        try:
                            send_json(client_socket, message)
                            response = receive_json(client_socket)
                            if response:
                                await response_queue.put(response)
                        except (ConnectionResetError, BrokenPipeError):
                            print(f"Connection to {server_host} for sending failed. Retrying...")
                            break
                    await asyncio.sleep(0.1)
            elif mode == "receiving":
                while True:
                    response = receive_json(client_socket)
                    if response is None:
                        print(f"No response from server, reconnecting...")
                        break
                    await response_queue.put(response)
                    await asyncio.sleep(0.1)

            break  # Salir del bucle de reintentos si la conexión es exitosa

        except (ConnectionRefusedError, ConnectionResetError, BrokenPipeError) as e:
            print(f"Connection to {server_host} for {mode} failed: {e}. Retrying in 0.5 seconds...")
            await asyncio.sleep(0.5)
            attempts += 1

        finally:
            if client_socket:
                client_socket.close()

    if attempts >= max_attempts:
        print(f"Failed to connect to {server_host} after {max_attempts} attempts. Exiting...")
        exit(1)

# Tarea asincrónica para manejar la conexión del servidor
async def server_task(host, port, mode):
    server_socket = create_socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"{host} is listening on port {port} for {mode}")

    while True:
        client_socket, addr = await asyncio.get_event_loop().run_in_executor(None, server_socket.accept)
        print(f"Connection from {addr}")
        asyncio.create_task(handle_client(client_socket, mode))

# Función para manejar la comunicación con el cliente
async def handle_client(client_socket, mode):
    try:
        while True:
            if mode == "sending":
                response = await response_queue.get()
                send_json(client_socket, response)
            elif mode == "receiving":
                data = client_socket.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))
                print(f"Received: {message}")
                response = {"status": "ok"}
                send_json(client_socket, response)
    finally:
        client_socket.close()

# Funciones auxiliares
async def send_custom_message(client_name, message, message_type="state"):
    print(" paso por funcion send_custom_message")
    """Función para enviar un mensaje personalizado."""
    message_data = {
        "sender": client_name,
        "message": message,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "type": message_type  # Añadir tipo de mensaje
    }
    await send_queue.put(message_data)

async def get_response():
    print(" paso por funcion get_response")
    """Función para obtener la respuesta más reciente."""
    try:
        return await asyncio.wait_for(response_queue.get(), timeout=10)
    except asyncio.TimeoutError:
        return None

async def participar_en_consenso(hexapodo_1):
    print(" paso por participar_en_consenso")
    
    print(f"[CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")

    state_message = {
        "type": "state",
        "data": hexapodo_1.compartir_estado()
    }
    await send_custom_message(client_name, json.dumps(state_message))

    await communication_ready.wait()
    response = await get_response()

    if response:
        if "data" in response:
            recibido = response["data"]
            print(f"Received state from other hexapod: {recibido}")

        else:
            print("Received response does not contain 'data'.")
    else:
        print("No response received.")

    hexapodo_2_id = int(list(recibido.keys())[0])
    hexapodo_1.comprobar_y_corregir_UID([hexapodo_2_id])

    new_recibido = {int(key): value for key, value in recibido.items()}

    hexapodo_2_estado = new_recibido
    hexapodo_1.elegir_lider([hexapodo_2_estado])

    print(f"[CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    return hexapodo_1
    
async def generar_rutina_de_baile():
    print(" paso por funcion generar_rutina_baile")
    numero_bailes = 6
    baile = crea_rutina(numero_bailes)
    mitad = len(baile) // 2
    subrutina1 = baile[:mitad]
    subrutina2 = baile[mitad:]
    return subrutina1, subrutina2

async def ejecutar_subrutina(subrurina):
    print(" paso por funcion ejecutar_subrutina")
    b = bailes()
    for baile in subrurina:
        metodo = getattr(b, baile)
        metodo()

# Función principal
async def main():
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

    print(raspberrypi_name)
    print(client_name)
    print(server_host)

    asyncio.create_task(server_task(raspberrypi_name, SERVER_SEND_PORT, "sending"))
    asyncio.create_task(server_task(raspberrypi_name, SERVER_RECEIVE_PORT, "receiving"))

    asyncio.create_task(client_task_with_ready(client_name, server_host, SERVER_RECEIVE_PORT, "sending", send_queue, response_queue))
    asyncio.create_task(client_task_with_ready(client_name, server_host, SERVER_SEND_PORT, "receiving", asyncio.Queue(), response_queue))

    while h1.max_completions > h1.completes and h1.max_tries > h1.tries and h1.energy > 0:
        if not h1.beliefs.beliefs[BDI_Actions.ACOMPAÑADO] and not comunicación:
            print(f"[INFO] El agente no está acompañado!")
            print(f"[COMUNICACIÓN] Buscando a alguien para balar el pasito perrón")
            comunicación = True
            env.buddy_here = True
            print(f"[COMUNICACIÓN] Comunicación establecida exitosamente con otro agente")
        if not comunicación:
            print(f"[ERROR] No se pudo establecer la comunicación con nadie")
            print(f"[ERROR] El agente no puede bailar solo")
            exit()
        
        print(f"[INFO] El agente está acompañado")
        print(f"[CONSENSO] Participando en el consenso")
        hexapodo_1 = await participar_en_consenso(hexapodo_1)
        
        if hexapodo_1.estado == role.LIDER:
            print(f"[BAILE] Generando rutina de baile")
            subrutina1, subrutina2 = await generar_rutina_de_baile()
            print(f"[BAILE] Rutina de baile generada")
            print(f"[BAILE] Subrutina 1 {subrutina1}")
            print(f"[BAILE] Subrutina 2 {subrutina2}")
            print(f"[BAILE] transmitiendo rutina de baile a los demás hexápodos")
            ... # Transmitir la rutina de baile a los demás hexápodos
            print(f"[BAILE] Rutina de baile transmitida exitosamente")
            print(f"[BAILE] Esperando confirmación de la rutina de baile")
            confirmacion_de_baile = True
            print(f"[BAILE] Confirmación de la rutina de baile recibida")
        else:
            print(f"[BAILE] Esperando la rutina de baile")
            ... # Esperar a recibir la rutina de baile
            print(f"[BAILE] Rutina de baile recibida")
            print(f"[BAILE] Enviando confirmación de la rutina de baile")
            ... # Enviar confirmación de la rutina de baile
            print(f"[BAILE] Confirmación de la rutina de baile enviada")
            confirmacion_de_baile = True
            subrutina1, subrutina2 = None
        
        if confirmacion_de_baile:
            print(f"[BAILE] Bailando subrutina 1")
            await ejecutar_subrutina(subrutina1)
            print(f"[BAILE] Subrutina 1 completada, enviando confirmación a los demás hexápodos")
            ...
            print(f"[BAILE] Confirmación de la subrutina 1 enviada")
            print(f"[BAILE] Esperando confirmación de la subrutina 1 de los demás hexápodos")
            confirmacion_de_subrutina_1 = True
            if not confirmacion_de_subrutina_1:
                ... # Esperar hasta recibirla
            print(f"[BAILE] Confirmación de la subrutina 1 recibida")
            print(f"[BAILE] Bailando subrutina 2")
            await ejecutar_subrutina(subrutina2)
            print(f"[BAILE] Subrutina 2 completada, enviando confirmación a los demás hexápodos")
            ...
            print(f"[BAILE] Confirmación de la subrutina 2 enviada")
            print(f"[BAILE] Esperando confirmación de la subrutina 2 de los demás hexápodos")
            confirmacion_de_subrutina_2 = True
            print(f"[BAILE] Confirmación de la subrutina 2 recibida")
            print(f"[INFO] Rutina completada")
            h1.completes += 1

if __name__ == '__main__':
    asyncio.run(main())
