from django.forms import ModelForm
from django import forms  
from .models import *

class ChatmessageCreateForm(ModelForm):
    body = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Add message...',
            'class': 'w-full p-3 text-white bg-gray-700 rounded-xl border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
            'maxlength': '300',
            'autofocus': True,
            'name': 'body'
        })
    )
    
    class Meta:
        model = GroupMessage
        fields = ['body']