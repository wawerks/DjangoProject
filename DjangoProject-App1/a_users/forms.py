from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'displayname', 'info']
        widgets = {
            'image': forms.FileInput(attrs={
                'id': 'profile-image-upload',
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'displayname': forms.TextInput(attrs={
                'placeholder': 'Add display name',
                'class': 'w-full p-2 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'info': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add information',
                'class': 'w-full p-2 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500'
            })
        }
        
class EmailForm(ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['email']
