from channels.generic.websocket import JsonWebsocketConsumer
from .generate_chat import chatgen

class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive_json(self, content):
        query = content['query']

        response = chatgen(query).removeprefix("1. ")

        self.send_json(content={
            "response": response,
        })

