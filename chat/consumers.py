import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from django.contrib.auth.models import User
from django.core.serializers import serialize

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.close()
    

    async def receive(self, text_data):
        text_data_json =  json.loads(text_data)
        print(text_data)
        message = text_data_json
        self.send(text_data=json.dumps({
            'message': message
        }))
        #print(message)
    

    async def send_message(self, event):
        data = event['message']
        print(data)
        await self.create_message(data=data)
        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):
        try:
            sender = User.objects.get(id=data['sender'])
            print(f"data is {data}")
            get_room_by_name = ChatGroup.objects.get(group_name=data['room_name'])
            if not Message.objects.filter(content=data['message']).exists():
                new_message = Message(group=get_room_by_name, sender=sender, content=data['message'])
                new_message.save()
                print(new_message)
        except Exception as e:
            print(f"Error creating message: {str(e)}")
        
           

    """
    def receive(self, *, text_data):
        if text_data.startswith("/name"):
            self.username = text_data[5:].strip()
            self.send(text_data="[set your username to %s]" % self.username)
        else:
            self.send(text_data=self.username + ": " + text_data)

    def disconnect(self, message):
        pass
    
    """

    """
        self.username = "Anonymous"
        self.accept()
        self.send(text_data="[Welcome %s!]" % self.username)

        get_room_by_name = ChatGroup.objects.get(group_name=data['room_name'])
        if not Message.objects.filter(content=data['message']).exists():
            new_message = Message(group=get_room_by_name, sender=data['sender'], content=data['message'])
            new_message.save()
            print(new_message)

        """