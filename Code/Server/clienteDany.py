import socket
import json
from time import sleep

def enviar_mensaje_cliente(server_socket, mensaje):
    # Convertir el mensaje a formato JSON
    mensaje_json = json.dumps(mensaje)
    
    # Enviar el mensaje JSON al servidor
    server_socket.sendall(mensaje_json.encode('utf-8'))
    print("Mensaje enviado al servidor.")

def recibir_mensaje_cliente(server_socket):
    # Recibir datos del servidor
    datos = server_socket.recv(1024).decode('utf-8')
    
    # Convertir los datos recibidos de JSON a un diccionario
    mensaje = json.loads(datos)
    
    print("Mensaje recibido del servidor:")
    print(mensaje)
    return mensaje

def conectar_cliente(host, port):
    host = 'hexapodo2.local'  # Cambia esto a la dirección IP de tu servidor
    port = 5000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Conectado al servidor en {host}:{port}")

    # Enviar confirmación al servidor
    client_socket.sendall("READY".encode('utf-8'))
    return port

if __name__ == "__main__":
    # Configuración del cliente
    host = 'hexapodo2.local'  # Cambia esto a la dirección IP de tu servidor
    port = 5000


    raspberrypi_name = socket.gethostname()
    if raspberrypi_name == 'hexapodo1':
            identificador = '1'
    else:
            identificador = '2'


    # Enviar y recibir mensajes en formato JSON
    mensaje_para_enviar = {
        "id": identificador,
        "estado": "candidato",
        "Lider": None
    }

    client_socket= conectar_cliente(host, port)

    
    enviar_mensaje_cliente(client_socket, mensaje_para_enviar)
    sleep(3)
    recibir_mensaje_cliente(client_socket)
    enviar_mensaje_cliente(client_socket, mensaje_para_enviar)

    #client_socket.close()