import requests
from cryptography.fernet import Fernet
from django.conf import settings

class App2Client:
    def __init__(self, base_url='http://localhost:8001'):
        self.base_url = base_url
        self.fernet = Fernet(settings.ENCRYPT_KEY)
        self.session = requests.Session()
        
    def encrypt_data(self, data):
        return self.fernet.encrypt(data.encode())
        
    def decrypt_data(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data).decode()
    
    def send_message(self, content, sender):
        """Send an encrypted message to App2"""
        endpoint = f"{self.base_url}/api/messages/"
        data = {
            'content': content,
            'sender': sender,
            'is_encrypted': True
        }
        
        # Encrypt the data
        encrypted_data = self.encrypt_data(str(data))
        
        # Send the encrypted data
        response = self.session.post(
            endpoint,
            data=encrypted_data,
            headers={'Content-Type': 'application/octet-stream'}
        )
        
        if response.status_code == 201:
            # Decrypt the response
            decrypted_response = self.decrypt_data(response.content)
            return decrypted_response
        else:
            raise Exception(f"Failed to send message: {response.status_code}")
    
    def get_responses(self, message_id):
        """Get responses for a specific message"""
        endpoint = f"{self.base_url}/api/messages/{message_id}/responses/"
        
        response = self.session.get(endpoint)
        if response.status_code == 200:
            # Decrypt the response
            decrypted_response = self.decrypt_data(response.content)
            return decrypted_response
        else:
            raise Exception(f"Failed to get responses: {response.status_code}")
