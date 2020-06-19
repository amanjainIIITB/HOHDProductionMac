from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print('fetch_message')
        print(data)
        messages = Message.get_all_messages(data['shop_id'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        # print('fetch_messages'+ str(content))
        self.send_message(content)

    def new_message(self, data):
        # author = data['from']
        # author_user = User.objects.filter(username=author)[0]
        author_user = data['from']
        print('new_message')
        print(author_user)
        print(data)
        message = Message.objects.create(
            author=author_user, 
            shopID = data['shop_id'],
            content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        print('messages_to_json')
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        print('message_to_json')
        return {
            'author': message.author,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Entry point of call flow to receive the message for both single send message or fetch all
    def receive(self, text_data):
        print('receive method')
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        

    #Send the message json created structure in chat window for single message
    def send_chat_message(self, message):    
        print('send_chat_message')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    #To send the message after page load
    def send_message(self, message):
        print('send_message')
        self.send(text_data=json.dumps(message))

    #to load the latest send message in chat
    def chat_message(self, event):
        print('chat_message')
        message = event['message']
        self.send(text_data=json.dumps(message))