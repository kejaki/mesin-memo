from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('class_name', 'nisn', 'angkatan', 'division', 'phone_number', 'email')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'class_name', 'profile_photo', 'angkatan', 'division']
        widgets = {
            'profile_photo': forms.FileInput(attrs={'accept': 'image/*'}),
        }
