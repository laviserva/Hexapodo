import socket
import json


host = '0.0.0.0'
#host = 'hexapodo2'
port = 5000
def enviar_mensaje_server(client_socket, mensaje):
    # Convertir el mensaje a formato JSON
    mensaje_json = json.dumps(mensaje)
    
    # Enviar el mensaje JSON al cliente
    client_socket.sendall(mensaje_json.encode('utf-8'))
    print("Mensaje enviado al cliente.")

def recibir_mensaje_server(client_socket):
    # Recibir datos del cliente
    datos = client_socket.recv(1024).decode('utf-8')
    
    # Convertir los datos recibidos de JSON a un diccionario
    mensaje = json.loads(datos)
    
    print("Mensaje recibido del cliente:")
    print(mensaje)
    return mensaje


def conectar_server(host,port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Esperando conexión en {host}:{port}...")

    client_socket, client_address = server_socket.accept()
    print(f"Conexión establecida desde {client_address}")

    # Esperar confirmación del cliente
    client_ready = client_socket.recv(1024).decode('utf-8')
    if client_ready == "READY":
        print("Cliente listo.")
        print(client_socket)
        mensaje = recibir_mensaje_server(client_socket)
        print(mensaje)
        # Recibir mensaje del cliente
        #mensaje_recibido = recibir_mensaje_server(client_socket)
        
        
        # Responder con un mensaje al cliente
        """mensaje_para_enviar = {
            "tipo": "respuesta",
            "contenido": "Hola, cliente!",
            "usuario": "servidor_1"
        }
        enviar_mensaje_server(client_socket, mensaje_para_enviar)"""
    else:
        print("Cliente no está listo.")
    return mensaje_recibido,client_socket, server_socket

if __name__ == "__main__":
    pass
    #client_socket, server_socket = conectar_server(host,port)

    #client_socket.close()
    #server_socket.close()