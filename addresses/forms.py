from django import forms
from .models import Address
from .views import check_address_by_zipcode


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Address
        fields = (
            "full_address",
            "detail_address",
            "extra_address",
            "sido",
            "sigungu",
            "zipcode",
            "is_jeju_mountain",
        )
        widgets = {
            "detail_address": forms.TextInput(attrs={"placeholder": "나머지 상세주소를 입력하세요"}),
            "sido": forms.HiddenInput,
            "sigungu": forms.HiddenInput,
            "extra_address": forms.HiddenInput,
            "zipcode": forms.HiddenInput,
            "is_jeju_mountain": forms.HiddenInput,
        }

        labels = {"full_address": "주소", "detail_address": ""}

    def clean_is_jeju_mountain(self):
        zipcode = self.cleaned_data["zipcode"]

        return check_address_by_zipcode(int(zipcode))
