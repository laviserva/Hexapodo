from hexapodocommunicatorzmq import HexapodCommunicator
import socket
import asyncio
import datetime

async def custom_message_sender(communicator):
    """Función para enviar mensajes personalizados en diferentes momentos."""
    await asyncio.sleep(5)  # Esperar a que la conexión se establezca

    print("Starting custom_message_sender coroutine...")

    while not communicator.connection_confirmed:
        print("Waiting for connection to be confirmed...")
        await asyncio.sleep(1)  # Espera hasta que la conexión esté confirmada

    print("Connection confirmed, starting to send messages...")

    message_count = 0

    while True:
        # Ejemplo de mensaje MOVE_FORWARD
        move_message = {
            "sender": communicator.name,
            "message": "MOVE_FORWARD",
            "parameters": {"speed": 5, "duration": 10},
            "timestamp": datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S'),
            "message_number": message_count
        }
        print(f"Preparing to send message: {move_message}")
        await communicator.send_message(move_message)
        print(f"Sent message: {move_message}")
        message_count += 1

        # Espera antes de enviar el próximo mensaje
        await asyncio.sleep(10)  # Envía un mensaje cada 10 segundos

def main():
    raspberrypi_name = socket.gethostname()

    # Configuración para hexápodo 1
    if raspberrypi_name == 'hexapodo1':
        send_port = 8765
        receive_port = 8766
        peer_send_uri = 'ws://hexapodo2.local:8765'
        peer_receive_uri = 'ws://hexapodo2.local:8766'

    # Configuración para hexápodo 2
    else:
        send_port = 8766
        receive_port = 8765
        peer_send_uri = 'ws://hexapodo1.local:8766'
        peer_receive_uri = 'ws://hexapodo1.local:8765'

    # Imprime las variables para verificar
    print(f"Raspberry Pi Name: {raspberrypi_name}")
    print(f"Send Port: {send_port}")
    print(f"Receive Port: {receive_port}")
    print(f"Peer Send URI: {peer_send_uri}")
    print(f"Peer Receive URI: {peer_receive_uri}")

    communicator = HexapodCommunicator(raspberrypi_name, send_port, receive_port, peer_send_uri, peer_receive_uri)
    
    loop = asyncio.get_event_loop()
    
    # Inicia la comunicación
    loop.create_task(communicator.start())

    # Inicia el envío de mensajes personalizados desde main
    loop.create_task(custom_message_sender(communicator))
    
    loop.run_forever()

if __name__ == "__main__":
    main()
