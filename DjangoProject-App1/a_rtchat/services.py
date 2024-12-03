import requests
import json
from django.conf import settings

class MessageService:
    def __init__(self):
        self.base_url = "http://localhost:8081"  # Updated to match App2's port

    def store_message(self, sender, receiver, content):
        """Send message to App2 for storage"""
        url = f"{self.base_url}/api/messages/store/"
        data = {
            'sender': sender,
            'receiver': receiver,
            'content': content
        }
        try:
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            print(f"Error storing message: {str(e)}")
            return None

    def get_messages(self, user):
        """Retrieve messages for a user from App2"""
        url = f"{self.base_url}/api/messages/"
        params = {'user': user}
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            print(f"Error retrieving messages: {str(e)}")
            return None
