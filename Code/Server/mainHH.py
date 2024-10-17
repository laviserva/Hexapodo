from HexapodoComunicator import HexapodoComunicator
import socket

def main():
    raspberrypi_name = socket.gethostname()

    # Configuración dinámica basada en el nombre de host
    if raspberrypi_name == 'hexapodo1':
        server_host = 'hexapodo2.local'
        client_name = 'hexapodo1.local'
    elif raspberrypi_name == 'hexapodo2':
        server_host = 'hexapodo1.local'
        client_name = 'hexapodo2.local'

    communicator = HexapodoComunicator(client_name, server_host)

    # Personalizar el mensaje a enviar
    custom_message = {"command": "move", "parameters": {"direction": "forward", "steps": 5}}

    # Enviar mensaje personalizado una vez
    received_message = communicator.exchange_data(custom_message)
    print(f"Mensaje recibido: {received_message}")

    custom_message = {"command": "move", "parameters": {"direction": "forward", "steps": 5}}

    # Enviar mensaje personalizado una vez
    received_message = communicator.exchange_data(custom_message)
    print(f"Mensaje recibido despues zz: {received_message}")


    # O ejecutar la tarea con iteraciones y mensajes generados automáticamente
#    communicator.execute_task(iterations=3)

if __name__ == "__main__":
    main()
