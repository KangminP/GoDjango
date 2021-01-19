from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Message
from django.forms import ModelChoiceField



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'last_name', 'first_name', 'pick']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '보낼 메시지를 입력하세요.',
                }
            ),
        }