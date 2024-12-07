from cryptography.fernet import Fernet
from django.conf import settings
import json

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.fernet = Fernet(settings.ENCRYPT_KEY)

    def __call__(self, request):
        # Only process API requests
        if request.path.startswith('/api/'):
            # Decrypt incoming request body if it exists
            if request.body:
                try:
                    encrypted_data = request.body
                    decrypted_data = self.fernet.decrypt(encrypted_data)
                    request._body = decrypted_data
                except Exception as e:
                    print(f"Decryption error: {e}")

        response = self.get_response(request)

        # Encrypt response data for API responses
        if request.path.startswith('/api/'):
            if hasattr(response, 'content'):
                try:
                    content = response.content
                    encrypted_content = self.fernet.encrypt(content)
                    response.content = encrypted_content
                except Exception as e:
                    print(f"Encryption error: {e}")

        return response
