from django import forms
from .models import Editor_Reviews


class PostForm(forms.ModelForm):

    class Meta:
        model = Editor_Reviews
        fields = ['title_text', 'content_text']
