import socket
import platform
import time

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 50000))  # Escucha en todas las interfaces en el puerto 50000
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print("Servidor de descubrimiento en espera...")
    
    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"Descubierto por {addr}")
        if data == b'discover_request':
            response_message = b'discover_response'
            server_socket.sendto(response_message, addr)
            return addr[0], server_socket.getsockname()[0]  # Devuelve IP del cliente, IP del servidor

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    broadcast_address = ('<broadcast>', 50000)  # Puerto conocido para el servicio de descubrimiento
    client_socket.sendto(b'discover_request', broadcast_address)

    print("Solicitud de descubrimiento enviada...")
    
    try:
        client_socket.settimeout(5)  # Esperar hasta 5 segundos por una respuesta
        data, addr = client_socket.recvfrom(1024)
        if data == b'discover_response':
            print(f"Servicio descubierto en {addr}")
            return client_socket.getsockname()[0], addr[0]  # Devuelve IP del cliente, IP del servidor
    except socket.timeout:
        print("Tiempo de espera agotado. No se encontraron más respuestas.")
        return None, None

if __name__ == "__main__":
    system_os = platform.system()
    
    if system_os == 'Windows':
        print("[Servidor]: Configurando este dispositivo como servidor...")
        ip_client, ip_server = server()
    else:
        print("[Cliente]: Configurando este dispositivo como cliente...")
        ip_client, ip_server = client()
    
    print(f"IP del Cliente: {ip_client}, IP del Servidor: {ip_server}")
