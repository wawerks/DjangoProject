from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from .services import MessageService

class App2StatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_service = MessageService()

    def __call__(self, request):
        # Get current URL name
        url_name = resolve(request.path_info).url_name
        
        # List of URLs that require App2 to be running
        protected_urls = ['home', 'chat']
        
        # Check if current URL requires App2
        if url_name in protected_urls:
            # Try to get messages to check if App2 is running
            response = self.message_service.get_messages('public-chat')
            if response.get('status') == 'error':
                # If not logged in, redirect to login page with error
                if not request.user.is_authenticated:
                    return HttpResponseRedirect(reverse('account_login') + '?error=server_down')
                # If logged in, show error page
                return render(request, 'error.html', {
                    'error_title': 'Server Not Available',
                    'error_message': 'The message server is currently not running. Please try again later.'
                })

        return self.get_response(request)
