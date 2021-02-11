from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('full_address', 'detail_address', 'extra_address', 'sido', 'sigungu')
        widgets = {
            'detail_address': forms.TextInput(attrs={'placeholder': '나머지 상세주소를 입력하세요'}),
            'sido': forms.HiddenInput,
            'sigungu': forms.HiddenInput,
            'extra_address': forms.HiddenInput,
        }
        
        labels = {
            'full_address': '주소',
            'detail_address': ''
        }