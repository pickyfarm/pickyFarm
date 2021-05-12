from django import forms
from .models import Question

class Question_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
    
    class Meta:
        model = Question
        fields = ('title', 'image', 'content')
        labels = {
            'title' : '제목',
            'image' : '첨부 이미지',
            'content' : '',
        }