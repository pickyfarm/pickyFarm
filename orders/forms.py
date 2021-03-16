from .models import Order_Group, Order_Detail
from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class Order_Group_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['rev_loc_detail'].widget.attrs['placeholder'] = '예)공동현관 앞에 놓아주세요'
        self.fields['rev_message'].widget.attrs['placeholder'] = '예)공동현관 비밀번호는 1234*입니다'
        self.fields['to_farm_message'].widget.attrs['placeholder'] = '예)수고 많으세요! 예쁘게 포장 부탁드려요~'

    PAYMENT_TYPES = (
        ('무통장 입금', '무통장 입금'),
        ('신용카드', '신용카드'),
    )

    REV_LOC_ATS = {
        ('기타장소', '기타장소'),
        ('경비실', '경비실'),
        ('택배함', '택배함'),
        ('문 앞', '문 앞'),
    }

    payment_type = forms.ChoiceField(choices=PAYMENT_TYPES, label="결제 수단", widget=forms.RadioSelect)
    rev_loc_at = forms.ChoiceField(
        label="받으실 장소", choices=REV_LOC_ATS, widget=forms.RadioSelect)


    class Meta:
        model = Order_Group
        fields = ('rev_name', 'rev_phone_number', 'rev_loc_at',
                  'rev_loc_detail', 'rev_message', 'to_farm_message', 'payment_type', )
        labels = {
            'rev_name': '이름',
            'rev_phone_number': '휴대폰',
            'rev_loc_at': '받으실 장소',
            'rev_loc_detail': '기타장소 세부사항',
            'rev_message': '배송지 특이사항',
            'to_farm_message': '농가 전달 메세지',
            'payment_type': '결제 수단',
        }
        widgets = {
            'rev_loc_detail': forms.TextInput(attrs={'required':'False'}),
            'rev_message': forms.TextInput(attrs={'required':'False'}),
            'to_farm_message': forms.TextInput(attrs={'required':'False'})

        }

    # def clean_product(self):
    #     product = self.cleaned_data.get('product')
    #     if product is None:
    #         return None
    #     else:
    #         return product

    # def clean_farm(self):
    #     farm = self.cleaned_data.get('farm')
    #     if farm is None:
    #         return None
    #     else:
    #         return farm
