import threading
import socket
from server import server_thread
from client import client_thread

SERVER_SEND_PORT = 65432
SERVER_RECEIVE_PORT = 65433

if __name__ == "__main__":
    raspberrypi_name = socket.gethostname()
    if raspberrypi_name == 'hexapodo1':
        server_host = 'hexapodo2.local'
        client_name = 'hexapodo1.local'
    else:
        server_host = 'hexapodo1.local'
        client_name = 'hexapodo2.local'

    threading.Thread(target=server_thread, args=(raspberrypi_name, SERVER_SEND_PORT, "sending")).start()
    threading.Thread(target=server_thread, args=(raspberrypi_name, SERVER_RECEIVE_PORT, "receiving")).start()
    threading.Thread(target=client_thread, args=(client_name, server_host, SERVER_RECEIVE_PORT, "sending")).start()
    threading.Thread(target=client_thread, args=(client_name, server_host, SERVER_SEND_PORT, "receiving")).start()
