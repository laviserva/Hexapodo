import socket
import json

SECRET_KEY = "my_secret_key"

# Función para crear sockets
def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Función para serializar datos a un formato JSON-serializable
def to_serializable(data):
    if hasattr(data, "__dict__"):  # Verifica si es un objeto con __dict__
        data = data.__dict__  # Convierte el objeto a un diccionario
    return data  # Devuelve el objeto serializable

# Función para deserializar datos JSON a objetos o estructuras de datos Python
def from_serializable(data, cls=None):
    if cls:
        # Si se proporciona una clase, reconvierte el diccionario en un objeto de esa clase
        obj = cls()
        obj.__dict__.update(data)
        return obj
    return data  # Devuelve el diccionario tal cual si no se proporciona una clase

# Función para enviar datos como texto JSON
def send_json(sock, data):
    serializable_data = to_serializable(data)  # Convertir a JSON-serializable
    json_data = json.dumps(serializable_data)  # Serializar a JSON
    sock.sendall(json_data.encode('utf-8'))  # Enviar los datos JSON como texto

# Función para recibir datos como texto JSON
def receive_json(sock):
    try:
        data = sock.recv(1024)  # Recibir datos
        if not data:
            print("Received empty message.")
            return None
        json_data = json.loads(data.decode('utf-8'))  # Decodificar los datos JSON
        return json_data  # Devuelve el diccionario o lista Python
    except (json.JSONDecodeError, ConnectionResetError, ConnectionAbortedError, TimeoutError) as e:
        print(f"Error decoding JSON response: {e}")
        return None

# Función para autenticar un cliente en el servidor usando una clave secreta
def authenticate(sock):
    auth_message = {"auth": SECRET_KEY}
    send_json(sock, auth_message)  # Envía el mensaje de autenticación
    response = receive_json(sock)  # Recibe la respuesta del servidor
    if response and response.get("status") == "ok":
        return True  # Autenticación exitosa
    return False  # Fallo en la autenticación
