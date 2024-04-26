import json
import os
import socket
import platform

from abc import ABC, abstractmethod
from load_configuration import ConfigManager
from camera import CameraSingletonFactory

class Communication(ABC):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None

    @abstractmethod
    def connect(self):
        pass

    def send(self, message: str):
        """Send a message to the other device
        
        Arguments:
            message {str} -- Message to send with the following format
            'command: *arguments'
        """
        self.socket.sendall(message.encode('utf-8'))
    
    def send_image(self):
        """Send an image to the other device with a type prefix."""
        try:
            self.camera = CameraSingletonFactory.get_camera("RGB888", (640, 480))
            image = self.camera.capture_image_as_array()
            image_bytes = image.tobytes()
            header = 'IMG'.encode('utf-8')
            message = header + len(image_bytes).to_bytes(4, 'big') + image_bytes
            self.socket.sendall(len(message).to_bytes(4, 'big'))
            self.socket.sendall(message)
        except Exception as e:
            print(f"Error sending image: {e}")

    
    def receive_image(self):
        """Receive an image from the other device and return it as byte data."""
        try:
            # Recibir el tamaño total de la imagen
            length = int.from_bytes(self.socket.recv(4), 'big')
            image_data = b''
            while len(image_data) < length:
                packet = self.socket.recv(4096)
                if not packet:
                    break
                image_data += packet

            return image_data
        except Exception as e:
            print(f"Error during image reception: {e}")
            return None

    def receive(self):
        """Receive data from the other device and handle based on type."""
        try:
            # Primero, recibimos el tamaño total del mensaje
            length = int.from_bytes(self.socket.recv(4), 'big')
            data = self.socket.recv(length)
            # Determinamos el tipo de mensaje de los primeros 3 bytes
            message_type = data[:3].decode('utf-8')

            # Redirigimos el procesamiento basándonos en el tipo de mensaje
            if message_type == 'IMG':
                return self.receive_image(data[3:])
            else:
                return data.decode('utf-8')
        except Exception as e:
            print(f"Error during receive: {e}")
            return None
    
    def process(self, request: json, interacciones: list):
        """Process the request and execute the command.
        
        Arguments:
            request {json} -- Request with the following format
            {command: *arguments}
            interacciones {list} -- List of possible interactions with the robot
        
        Request structure:
            {
                1: [command, *args],
                2: [command, *args]
            }
        """
        inter_names = [type(n).__name__ for n in interacciones]
        
        for command_id in sorted(request, key=lambda x: int(x)):
            command_name, *args = request[command_id]
            command_name = command_name.replace('-', '.')
            command_name, method = command_name.split('.')
            command_name = command_name.capitalize()
            print(f"[Cliente]: Comando: {command_name}, Método: {method}, Argumentos: {args}")
            print("[Cliente]: Interacciones disponibles:", inter_names)
            print("[Cliente]: ", inter_names.index(command_name))
            print("[Cliente]: ", interacciones[inter_names.index(command_name)])

            # verifiquemos que exista la clase y el método en comando
            if command_name in inter_names:
                if not method in dir(interacciones[inter_names.index(command_name)]):
                    print(f"[Cliente]: El método {method} no está disponible en {command_name}")
                method_ex = getattr(interacciones[inter_names.index(command_name)], method)
                print(f"[Cliente]: nombre de metodo: {method_ex.__name__}")
                out = method_ex(*args)
                print(f"Resultado de la operación: {out}")

        self.send_image()

    def get_data(self):
        try:
            data = self.receive()
            print("Datos recibidos:", data)
            return data
        except Exception as e:
            print(f"Error al recibir datos: {e}")

    def from_json_to_str(self, json_data):
        return json.dumps(json_data)

    def close_connection(self):
        self.socket.close()

class Server(Communication):
    """Windows PC"""
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        print("[Servidor]: Esperando conexiones...")
        conn, addr = self.socket.accept()
        print(f"[Servidor]: Conexión establecida desde {addr}")
        #conn.close()
        return self.socket, conn

class Client(Communication):
    "Raspberry Pi"
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[Cliente]: Tratando de conectar con el servidor")
        self.socket.connect((self.ip, self.port))
        print("[Cliente]: Conectado!")
        return self

def run_server(ip, port):
    server = Server(ip, port)
    return server.connect()

def run_client(ip, port):
    client = Client(ip, port)
    conn = client.connect()
    return client, conn

if __name__ == "__main__":
    system_os = platform.system()
    config = ConfigManager.get_config()
    port = int(config['CONNECTION']['PORT'])

    if system_os == 'Windows':
        print("[Servidor]: Configurando este dispositivo como servidor...")
        ip = '0.0.0.0'
        run_server(ip = ip, port = port)
    else:
        print("[Cliente]: Configurando este dispositivo como cliente...")
        ip = config['CONNECTION']['IP']
        print(f"Conectando a {ip}:{port}")
        run_client(ip=ip, port=port)