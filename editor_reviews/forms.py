from django import forms
from .models import Editor_Review
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from products.models import Category, Product
from users.models import Farmer


class Editors_Reviews_Form(forms.ModelForm):

    POST_CAT = (
        ('farm_cover', '농가 취재기'),
        ('products', '못난이 농산물'),
        ('recipe', '요리/레시피'),
    )

    # title = forms.CharField(label="제목")
    # contents = forms.CharField(widget=SummernoteWidget(), label="")
    # main_image = forms.ImageField(label="썸네일")
    post_category = forms.ChoiceField(choices=POST_CAT, label="포스팅 카테고리")
    farm = forms.ModelChoiceField(required=False, label="관련 농가", empty_label='--관련 농가 선택--', queryset=Farmer.objects.all())
    product = forms.ModelMultipleChoiceField(required=False, label="연관 작물", queryset=Product.objects.filter(
        open=True), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Editor_Review
        fields = ('title', 'sub_title', 'contents', 'main_image',
                  'post_category', 'farm', 'product')
        labels = {
            'title': '제목',
            'sub_title' : '부제목',
            'contents': '',
            'main_image': '썸네일',
            # 'post_category': '카테고리',
            # 'product': '관련 작물',
        }
        widgets = {
            'contents': SummernoteWidget(),
        }

    def clean_product(self):
        product = self.cleaned_data.get('product')
        if product is None:
            return None
        else:
            return product
    
    def clean_farm(self):
        farm = self.cleaned_data.get('farm')
        if farm is None:
            return None
        else:
            return farm
