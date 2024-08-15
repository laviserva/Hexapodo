import asyncio
import websockets
import json
import datetime

class HexapodCommunicator:
    def __init__(self, name, send_port, receive_port, peer_send_uri, peer_receive_uri):
        self.name = name
        self.send_port = send_port
        self.receive_port = receive_port
        self.peer_send_uri = peer_send_uri
        self.peer_receive_uri = peer_receive_uri
        self.sender_socket = None
        self.receiver_socket = None
        self.connection_confirmed = False
        self.reconnecting = False

    async def start_send_server(self):
        """Inicia el servidor WebSocket para aceptar conexiones entrantes en el puerto de envío."""
        try:
            print(f"Attempting to start send server on port {self.send_port}")
            server = await websockets.serve(self.handle_send_connection, "0.0.0.0", self.send_port)
            print(f"Send WebSocket server started on ws://0.0.0.0:{self.send_port}")
            await server.wait_closed()
        except Exception as e:
            print(f"Failed to start send server on port {self.send_port}: {e}")

    async def start_receive_server(self):
        """Inicia el servidor WebSocket para aceptar conexiones entrantes en el puerto de recepción."""
        try:
            print(f"Attempting to start receive server on port {self.receive_port}")
            server = await websockets.serve(self.handle_receive_connection, "0.0.0.0", self.receive_port)
            print(f"Receive WebSocket server started on ws://0.0.0.0:{self.receive_port}")
            await server.wait_closed()
        except Exception as e:
            print(f"Failed to start receive server on port {self.receive_port}: {e}")

    async def handle_send_connection(self, websocket, path):
        """Maneja las conexiones entrantes en el servidor de envío."""
        print(f"New send connection established from {websocket.remote_address}")
        await self.confirm_connection(websocket)
        try:
            async for message in websocket:
                print(f"Received in send server: {message}")
                await self.handle_received_message(message)
        except websockets.ConnectionClosed:
            print(f"Send connection closed by {websocket.remote_address}")
        except Exception as e:
            print(f"Error in send connection: {e}")

    async def handle_receive_connection(self, websocket, path):
        """Maneja las conexiones entrantes en el servidor de recepción."""
        print(f"New receive connection established from {websocket.remote_address}")
        await self.confirm_connection(websocket)
        self.receiver_socket = websocket  # Asigna el socket de recepción
        await self.receive_messages()  # Llama directamente al método de recepción

    async def connect_to_send_peer(self):
        """Conecta al servidor WebSocket en el puerto de envío del peer."""
        while not self.connection_confirmed or self.reconnecting:
            try:
                print(f"Attempting to connect to peer's send server at {self.peer_send_uri}")
                self.sender_socket = await websockets.connect(self.peer_send_uri)
                print(f"Connected to peer's send server at {self.peer_send_uri}")
                await self.confirm_connection(self.sender_socket)
                self.reconnecting = False
                break
            except (ConnectionRefusedError, OSError) as e:
                print(f"Connection to send peer failed: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)

    async def connect_to_receive_peer(self):
        """Conecta al servidor WebSocket en el puerto de recepción del peer."""
        while not self.connection_confirmed or self.reconnecting:
            try:
                print(f"Attempting to connect to peer's receive server at {self.peer_receive_uri}")
                self.receiver_socket = await websockets.connect(self.peer_receive_uri)
                print(f"Connected to peer's receive server at {self.peer_receive_uri}")
                await self.confirm_connection(self.receiver_socket)
                self.reconnecting = False
                await self.receive_messages()  # Llama directamente al método de recepción
                break
            except (ConnectionRefusedError, OSError) as e:
                print(f"Connection to receive peer failed: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)

    async def confirm_connection(self, websocket):
        """Intercambia mensajes de confirmación de conexión."""
        confirmation_message = {
            "sender": self.name,
            "message": "Connection Confirmed",
            "timestamp": datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')
        }
        await websocket.send(json.dumps(confirmation_message))
        print(f"Sent confirmation message from {self.name}")

        response = await websocket.recv()
        response_data = json.loads(response)
        if response_data.get("message") == "Connection Confirmed":
            self.connection_confirmed = True
            print(f"Connection with {response_data['sender']} confirmed!")

    async def send_message(self, message):
        """Envía un mensaje al peer."""
        if self.sender_socket and self.connection_confirmed:
            await self.sender_socket.send(json.dumps(message))
            print(f"Sent: {message}")
        else:
            print("Sender socket is not connected or connection not confirmed.")

    async def receive_messages(self):
        """Recibe múltiples mensajes del peer."""
        while self.receiver_socket:
            try:
                print("Waiting for messages...")
                message = await self.receiver_socket.recv()
                print(f"Received: {message}")
                await self.handle_received_message(message)
            except websockets.ConnectionClosed:
                print("Receiver socket closed.")
                self.reconnecting = True
                self.receiver_socket = None  # Reinicia el socket de recepción al cerrarse
                break
            except Exception as e:
                print(f"Error in receive_messages: {e}")
                self.receiver_socket = None  # Reinicia el socket de recepción en caso de error
                break
            await asyncio.sleep(1)

    async def handle_received_message(self, message):
        """Procesa los mensajes recibidos."""
        data = json.loads(message)
        print(f"Processing message from {data['sender']}: {data}")

    def start(self):
        """Inicia los servidores y los clientes."""
        loop = asyncio.get_event_loop()

        # Inicia los servidores WebSocket en ambos puertos
        loop.create_task(self.start_send_server())
        loop.create_task(self.start_receive_server())

        # Conecta a los servidores de envío y recepción del peer
        loop.create_task(self.connect_to_send_peer())
        loop.create_task(self.connect_to_receive_peer())

        loop.run_forever()
