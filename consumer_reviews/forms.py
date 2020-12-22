from django import forms
from .models import Consumer_Reviews


class PostForm(forms.ModelForm):

    class Meta:
        model = Consumer_Reviews
        fields = ['title_text', 'content_text']
