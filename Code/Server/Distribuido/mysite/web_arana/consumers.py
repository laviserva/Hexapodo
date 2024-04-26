import base64
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

class ConsumidorVotacion(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        print("conectasdo chat")
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))



class ConsumidorIMG(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print("conectado IMG")
        await self.accept()
        self.running = True
        while self.running:
            try:
                image_path = r'C:\Users\Pc-01\Documents\Hexapodo\Code\Server\Distribuido\mysite\web_arana\static\imgs\imagen.jpeg'
                with open(image_path, 'rb') as image_file:
                    encoded_string = base64.b64encode(
                        image_file.read()).decode('utf-8')
                await self.send(text_data=encoded_string)
            
            finally:
                await asyncio.sleep(2)
    async def disconnect(self, close_code):
        self.running = False
