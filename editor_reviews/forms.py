from django import forms
from .models import Editor_Reviews
from ckeditor.widgets import CKEditorWidget

class Editors_Reviews_Form(forms.ModelForm):
    
    # title = forms.CharField(label="제목")
    # contents = forms.CharField(widget=CKEditorWidget(), label="")
    # main_image = forms.ImageField(label="썸네일")
    # post_category = forms.ChoiceField(label="포스팅 카테고리")
    # product_category = forms.ChoiceField(label="작물 카테고리")
    # product = forms.ChoiceField(label="연관 작물")
    
    class Meta:
        model = Editor_Reviews
        fields=['title', 'contents', 'main_image', 'post_category', 'product_category', 'product']

