from django import forms
from .models import ProfilePhoto

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = ProfilePhoto
        fields = ['profile_picture']