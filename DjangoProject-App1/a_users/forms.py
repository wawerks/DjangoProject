from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from allauth.account.forms import SignupForm
import os

class ProfileForm(ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your first name',
            'class': 'w-full p-2 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your last name',
            'class': 'w-full p-2 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )

    class Meta:
        model = Profile
        fields = ['image', 'displayname', 'info']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'displayname': forms.TextInput(attrs={
                'placeholder': 'Add display name',
                'class': 'w-full p-2 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'required': False,
            }),
            'info': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add information',
                'class': 'w-full p-2 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'required': False,
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
        
        # Make sure displayname field is properly initialized
        self.fields['displayname'].required = False
        if self.instance and self.instance.displayname:
            self.fields['displayname'].initial = self.instance.displayname

        # Make all fields optional
        for field in self.fields:
            self.fields[field].required = False

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return None
        
        # Check file size (limit to 5MB)
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image file too large ( > 5MB )")
        
        # Check file extension
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
            raise forms.ValidationError("Unsupported file extension. Please use .jpg, .jpeg, .png, or .gif")
        
        return image

    def clean(self):
        cleaned_data = super().clean()
        # Check if any field has been modified
        has_changes = False
        
        print("\nForm Cleaning:")
        print(f"Display name in form: {cleaned_data.get('displayname')}")
        print(f"Display name in instance: {self.instance.displayname}")
        print(f"Raw POST data displayname: {self.data.get('displayname')}")
        
        if cleaned_data.get('image'):
            has_changes = True
            print("Image changed")
        if cleaned_data.get('displayname') != self.instance.displayname:
            print("Display name has changed")
            print(f"New display name: {cleaned_data.get('displayname')}")
            has_changes = True
        if cleaned_data.get('info') != self.instance.info:
            has_changes = True
            print("Info changed")
        if (cleaned_data.get('first_name') and 
            cleaned_data['first_name'] != self.user.first_name):
            has_changes = True
            print("First name changed")
        if (cleaned_data.get('last_name') and 
            cleaned_data['last_name'] != self.user.last_name):
            has_changes = True
            print("Last name changed")

        if not has_changes:
            raise forms.ValidationError("No changes were made to update.")
        
        return cleaned_data

    def save(self, commit=True):
        print("\nSaving form...")
        profile = super().save(commit=False)
        print(f"Profile before save - displayname: {profile.displayname}")
        
        # Save the user's first and last name
        if self.cleaned_data.get('first_name'):
            profile.user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data.get('last_name'):
            profile.user.last_name = self.cleaned_data['last_name']
            
        # Always set displayname from cleaned_data if it exists
        displayname = self.cleaned_data.get('displayname')
        if displayname is not None:
            print(f"Setting display name from cleaned data: {displayname}")
            profile.displayname = displayname
            
        if commit:
            print("Committing changes...")
            profile.user.save()
            profile.save()
            print(f"Profile after save - displayname: {profile.displayname}")
            
            # Verify in database
            from django.core.cache import cache
            cache.clear()  # Clear any cached data
            fresh_profile = type(profile).objects.get(pk=profile.pk)
            print(f"Fresh from database - displayname: {fresh_profile.displayname}")
            
        return profile


class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
