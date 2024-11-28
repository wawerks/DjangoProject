from django.forms import ModelForm
from django import forms  
from .models import *

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add message...',
                'class': 'w-full p-4 text-black rounded-xl',
                'maxlength': '300',
                'autofocus': True,
                'id': 'chat-message-input'
            })
        }