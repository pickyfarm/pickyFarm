from django import forms
from .models import Comment, Product_Comment, Editor_Review_Comment, Farmer_Story_Comment
from .models import Product_Recomment, Editor_Review_Recomment, Farmer_Story_Recomment

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text',]


class ProductCommentForm(forms.ModelForm):

    evaluate = (
        (1, "bad"),
        (3, "normal"),
        (5, "good"),
    )
    freshness = forms.ChoiceField(choices=evaluate, label="", widget=forms.RadioSelect)
    flavor = forms.ChoiceField(choices=evaluate, label="", widget=forms.RadioSelect)
    cost_performance = forms.ChoiceField(choices=evaluate, label="", widget=forms.RadioSelect)

    class Meta:
        model = Product_Comment
        fields = (
            "text",
            "freshness",
            "flavor",
            "cost_performance",
        )
        widgets = {
            "text": forms.Textarea(attrs={"placeholder": ""}),
            "freshness": forms.RadioSelect,
            "flavor": forms.RadioSelect,
            "cost_performance": forms.RadioSelect,
        }


class ProductRecommentForm(forms.ModelForm):
    class Meta:
        model = Product_Recomment
        fields = [
            "text",
        ]
        labels = {"text": ""}


class EditorReviewCommentForm(forms.ModelForm):
    class Meta:
        model = Editor_Review_Comment
        fields = ["text"]


class EditorReviewRecommentForm(forms.ModelForm):
    class Meta:
        model = Editor_Review_Recomment
        fields = [
            "text",
        ]


class FarmerStoryCommentForm(forms.ModelForm):
    class Meta:
        model = Farmer_Story_Comment
        fields = ["text"]


class FarmerStoryRecommentForm(forms.ModelForm):
    class Meta:
        model = Farmer_Story_Recomment
        fields = ["text"]
