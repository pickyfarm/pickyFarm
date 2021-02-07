from django import forms
from .models import Editor_Review
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from products.models import Category, Product


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
    product_category = forms.ModelChoiceField(required=False, label="작물 카테고리", queryset=Category.objects.filter(
        parent=None), empty_label='--관련 작물 카테고리 선택--')
    product = forms.ModelChoiceField(required=False, label="연관 작물", queryset=Product.objects.filter(
        open=True), empty_label='--관련 작물 선택--')

    class Meta:
        model = Editor_Review
        fields = ('title', 'contents', 'main_image',
                  'post_category', 'product_category', 'product')
        labels = {
            'title': '제목',
            'contents': '',
            'main_image': '썸네일',
            # 'post_category': '카테고리',
            # 'product_category': '관련 작물 종류',
            # 'product': '관련 작물',
        }
        widgets = {
            'contents': SummernoteWidget(),
        }

    def clean_product_category(self):
        product_category = self.cleaned_data.get('product_category')
        if product_category is None:
            return None
        else:
            return product_category

    def clean_product(self):
        product = self.cleaned_data.get('product')
        if product is None:
            return None
        else:
            return product
