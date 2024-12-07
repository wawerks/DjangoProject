from cryptography.fernet import Fernet
from django.conf import settings
import base64
import json
from django.http import JsonResponse
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Initialize encryption key - in production, this should be in environment variables
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def __call__(self, request):
        # Skip encryption for DRF browsable API
        if request.path.startswith('/api/') and 'text/html' in request.headers.get('Accept', ''):
            return self.get_response(request)

        # Skip encryption for API authentication endpoints
        if request.path in ['/api/token/', '/api/token/refresh/']:
            return self.get_response(request)

        if request.path.startswith('/api/'):
            # Decrypt incoming data if it's encrypted
            if request.method in ['POST', 'PUT', 'PATCH']:
                try:
                    if request.body:
                        encrypted_data = request.body
                        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                        request._body = decrypted_data
                except Exception as e:
                    return JsonResponse({'error': 'Invalid encrypted data'}, status=400)

        # Process the request
        response = self.get_response(request)

        # Skip encryption for DRF responses
        if isinstance(response, DRFResponse):
            return response

        # Encrypt outgoing data for non-DRF responses
        if request.path.startswith('/api/'):
            try:
                if hasattr(response, 'content'):
                    content = response.content
                    encrypted_content = self.cipher_suite.encrypt(content)
                    response.content = encrypted_content
            except Exception as e:
                return JsonResponse({'error': 'Encryption error'}, status=500)

        return response

    def get_encryption_key(self):
        """Return the current encryption key - useful for sharing with other application"""
        return base64.b64encode(self.key).decode('utf-8')
