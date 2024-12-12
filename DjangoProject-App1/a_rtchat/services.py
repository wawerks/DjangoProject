import requests
import json
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MessageService:
    def __init__(self):
        self.base_url = "http://localhost:8081"

    def store_message(self, sender, receiver, content):
        """Send message to App2 for storage"""
        url = f"{self.base_url}/api/messages/store/"
        data = {
            'sender': sender,
            'receiver': receiver,
            'content': content
        }
        try:
            response = requests.post(url, json=data, timeout=5)  # Add timeout
            response.raise_for_status()  # Raise error for bad status codes
            return response.json()
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error while storing message. Is App2 running on {self.base_url}?")
            return {'status': 'error', 'message': 'Connection failed'}
        except requests.exceptions.Timeout:
            logger.error("Timeout while storing message")
            return {'status': 'error', 'message': 'Request timed out'}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error storing message: {str(e)}")
            return {'status': 'error', 'message': str(e)}
        except Exception as e:
            logger.error(f"Unexpected error storing message: {str(e)}")
            return {'status': 'error', 'message': 'Internal server error'}

    def get_messages(self, user):
        """Retrieve messages for a user from App2"""
        url = f"{self.base_url}/api/messages/"
        params = {'user': user}
        try:
            response = requests.get(url, params=params, timeout=5)  # Add timeout
            response.raise_for_status()  # Raise error for bad status codes
            return response.json()
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error while getting messages. Is App2 running on {self.base_url}?")
            return {'status': 'error', 'message': 'Connection failed'}
        except requests.exceptions.Timeout:
            logger.error("Timeout while getting messages")
            return {'status': 'error', 'message': 'Request timed out'}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting messages: {str(e)}")
            return {'status': 'error', 'message': str(e)}
        except Exception as e:
            logger.error(f"Unexpected error getting messages: {str(e)}")
            return {'status': 'error', 'message': 'Internal server error'}