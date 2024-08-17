from hexapodocomunicator import HexapodCommunicator,custom_message_sender
import socket
import threading

SERVER_SEND_PORT = 65432
SERVER_RECEIVE_PORT = 65433

def main():
    raspberrypi_name = socket.gethostname()
    if raspberrypi_name == 'hexapodo1':
        server_host = 'hexapodo2.local'
        client_name = 'hexapodo1.local'
    else:
        server_host = 'hexapodo1.local'
        client_name = 'hexapodo2.local'

    communicator = HexapodCommunicator(client_name, server_host, SERVER_SEND_PORT, SERVER_RECEIVE_PORT)
    communicator.start()

    # Ejemplo de uso de la función de envío de mensajes personalizados
    threading.Thread(target=custom_message_sender, args=(communicator,)).start()

if __name__ == "__main__":
    main()
