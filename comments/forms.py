from django import forms
from .models import Comment, Product_Comment
from .models import Product_Recomment

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text',]

class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = Product_Comment
        fields=['text',]

# class EditorReviewCommentForm(forms.ModelForm):
#     class Meta:
#         model = Editor_Review_Comment
#         fields=['text',]

class ProductRecommentForm(forms.ModelForm):
    class Meta:
        model = Product_Recomment
        fields = ['text', ]

# class EditorReviewRecomment(forms.ModelForm):
#     class Meta:
#         model = Editor_Review_Recomment
#         fields = ['text',]