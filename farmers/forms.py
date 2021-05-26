from django import forms
from . import models
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

# farm 입점 관련
class FarmEnrollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = models.Farmer
        fields = (
            "farm_name",
            "farmer_profile",
            "farm_profile",
            "profile_title",
            "farm_desc",
            "farm_cat",
        )
        widgets = {
            "farm_cat": forms.RadioSelect,
            "profile_title": forms.TextInput(attrs={"placeholder": "농장을 한 문장으로 소개해주세요"}),
        }
        labels = {
            "farm_name": "농장 이름",
            "farmer_profile": "프로필 사진",
            "farm_profile": "농장 사진",
            "profile_title": "농장 한 줄 소개",
            "farm_desc": "농장 상세 소개",
            "farm_cat": "해시 태그 선택",
        }


class FarmApplyForm(forms.ModelForm):
    class Meta:
        model = models.Farm_Apply
        fields = (
            "name",
            "phone_num",
            "farm_name",
            "farm_cat",
            "detail_cat",
            "desc",
        )
        widgets = {
            "farm_cat": forms.RadioSelect,
            "detail_cat": forms.TextInput(attrs={"placeholder": "세부품목을 작성해주세요"}),
        }
        labels = {
            "name": "이름",
            "phone_num": "휴대폰 번호",
            "farm_name": "농장 이름",
            "farm_cat": "품종",
            "detail_cat": "",
            "desc": "추가 전달 사항",
        }


class FarmerStoryForm(forms.ModelForm):
    class Meta:
        model = models.Farmer_Story
        fields = (
            "title",
            "thumbnail",
            "content",
        )
        widgets = {
            "content": SummernoteWidget(),
        }
