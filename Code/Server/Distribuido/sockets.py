import socket
import platform

class Server:
    def __init__(self, client_adress:str= "raspberrypi.local", port:int = 54321) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[Servidor]: Conectando a {client_adress}:{port}")
        self.client_socket.connect((client_adress, port))

    def receive_message(self):
        print("[Servidor]: Esperando mensaje...")
        message = self.client_socket.recv(1024)
        message = message.decode()
        print(f"[Servidor]: Mensaje recibido: {message}")
        return message
    
    def close_connection(self):
        self.client_socket.close()

class Client:
    def __init__(self, server_adress:str = None, port = 54321):
        self.port = port
        if server_adress is None:
            server_adress = socket.gethostname()
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Obtén el nombre del host local
        hostname = socket.gethostname()
        self.local_ip = socket.gethostbyname(hostname + ".local")
    
    def bind_and_listen(self):
        # Asocia el socket a la dirección local y un puerto
        self.server_socket.bind((self.local_ip, self.port))
        self.server_socket.listen(5)

        print(f"[Cliente]: Escuchando en {self.local_ip}:{self.port}")

        while True:
            # Espera una conexión
            client_socket, addr = self.server_socket.accept()
            print(f"Conexión desde {addr}")
            
            # Envía un mensaje al cliente
            client_socket.sendall(b'Hola desde Raspberry Pi!')
            client_socket.close()
        

if __name__ == "__main__":
    if platform.system() == "Windows":
        server = Server()
        server.receive_message()
        server.close_connection()
    else:
        cliente = Client()
        cliente.bind_and_listen()