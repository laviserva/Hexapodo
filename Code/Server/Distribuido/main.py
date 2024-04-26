import json
import platform
import time

from load_configuration import ConfigManager
from sockets_connection import Server, Client

from sockets_connection import run_client, run_server

def server(connection):
    try:
        x, y, speed, angle = "0", "0", "7", "14" # angulo en radian
        print("hola mundo")

        data = {
                1: ["ctrl-avanzar", "15"],
                2: ["ctrl-girar", "90"],
                3: ["ctrl-girar", "-90"],
                4: ["ctrl-avanzar_hasta_obstaculo"],
                5: ["sound-play"],
                6: ["camera-save_image"]
                }
        json_data = json.dumps(data).encode('utf-8')
        connection.sendall(len(json_data).to_bytes(4, 'big'))
        connection.sendall(json_data)
        print("[Servidor]: Datos enviados.")

    finally:
        connection.close()

def client_method(client, interacciones):
    while True:
        try:
            socket = client.socket
            length = int.from_bytes(socket.recv(4), 'big')
            data = json.loads(socket.recv(length).decode('utf-8'))
            print("[Cliente]: Datos recibidos:", data)
            print("[Cliente]: Procesando datos...")
            client.process(data, interacciones)
        except Exception as e:
            print("[Cliente]: Error durante la recepción o procesamiento:", e)
            break

if __name__ == "__main__":
    system_os = platform.system()
    config = ConfigManager.get_config()
    port = int(config['CONNECTION']['PORT'])

    if system_os == 'Windows':
        print("[Servidor]: Configurando este dispositivo como servidor...")
        ip = "0.0.0.0"
        _, connection = run_server(ip, port) # socket, connection
        server(connection)
    else:
        from robot import Sound, Ctrl, Ultrasonic, Camera
        
        control = Ctrl()
        buzzer = Sound()
        ultrasonic = Ultrasonic()
        #camera = Camera()
        
        # Añadiendo todas las posibles interacciones del robot en el sistema distribuido para procesar los comandos en el cliente
        interacciones = [control, buzzer, ultrasonic]#, camera]
        print("[Cliente]: Configurando este dispositivo como cliente...")
        ip = config['CONNECTION']['IP']
        print(f"[Cliente]: Conectando a {ip}:{port}")

        reconexion = False
        while True:  # Intentar reconectar si la conexión se pierde
            try:
                client, _ = run_client(ip=ip, port=port)
                if reconexion:
                    print("[Cliente]: Conexión restablecida!")
                    reconexion = False
                else:
                    print("[Cliente]: Conectado!")
                client_method(client, interacciones)
            except Exception as e:
                reconexion = True
                print("[Cliente]:", e)
                print("[Cliente]: Error al conectar con el servidor, intentando reconectar", end="")
                for _ in range(5):
                    print(".", end="")
                    time.sleep(1)
                print()