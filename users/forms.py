from django import forms
from . import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.password_validation import validate_password
from django.forms.widgets import NumberInput
from django.contrib.auth.forms import PasswordResetForm
from django.templatetags.static import static
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class LoginForm(forms.Form):
    username = forms.CharField(
        label="아이디",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "아이디를 입력해주세요"}),
    )
    password = forms.CharField(
        label="비밀번호", widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 입력해주세요"})
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                raise models.User.DoesNotExist
        except models.User.DoesNotExist:
            raise ValidationError("가입하지 않은 ID거나 비밀번호가 틀렸습니다.")


GENDER_CHOICES = {
    ("male", "남성"),
    ("female", "여성"),
}


class SignUpForm(forms.Form):
    username = forms.CharField(
        label="아이디",
        max_length=100,
        label_suffix="",
        widget=forms.TextInput(attrs={"placeholder": "6자 이상의 영문 혹은 영문과 숫자를 조합"}),
    )
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 입력하세요"}),
        label_suffix="",
    )
    password_re = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 한번 더 입력하세요"}),
        label_suffix="",
    )

    account_name = forms.CharField(
        label="이름",
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "이름을 입력하세요"}),
        label_suffix="",
    )

    phone_number = forms.CharField(
        label="전화번호",
        max_length=11,
        widget=forms.TextInput(attrs={"placeholder": "숫자만 입력하세요"}),
        label_suffix="",
    )

    nickname = forms.CharField(
        label="닉네임",
        max_length=100,
        label_suffix="",
        widget=forms.TextInput(attrs={"placeholder": "부적절한 닉네임은 제재를 받을 수 있습니다"}),
    )
    email = forms.EmailField(label="이메일", label_suffix="")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = models.User.objects.get(username=username)
            raise ValidationError("중복된 아이디 입니다. 사용하실 수 없습니다")
        except ObjectDoesNotExist:
            return username

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if validate_password(password) == None:
            return password

        else:
            raise ValidationError("사용할 수 없는 비밀번호입니다.")

    def clean_password_re(self):
        password = self.cleaned_data.get("password")
        password_re = self.cleaned_data.get("password_re")
        if password == password_re:
            return password_re
        else:
            raise ValidationError("비밀번호가 일치하지 않습니다")

    def save(self):
        username = self.cleaned_data.get("username")
        password_re = self.cleaned_data.get("password_re")
        account_name = self.cleaned_data.get("account_name")
        phone_number = self.cleaned_data.get("phone_number")
        nickname = self.cleaned_data.get("nickname")
        email = self.cleaned_data.get("email")

        user = models.User.objects.create_user(
            username, email=email, password=password_re
        )

        user.first_name = ""
        user.last_name = ""
        user.account_name = account_name
        user.phone_number = phone_number
        user.nickname = nickname

        user.save()


class FindMyIdForm(forms.Form):
    account_name = forms.CharField(
        label="이름", widget=forms.TextInput(attrs={"placeholder": "이름을 입력해주세요"})
    )
    email = forms.EmailField(
        label="이메일", widget=forms.TextInput(attrs={"placeholder": "이메일을 입력해주세요"})
    )


class MyPasswordResetForm(PasswordResetForm):
    username = forms.CharField(
        label="아이디", widget=forms.TextInput(attrs={"placeholder": "아이디를 입력해주세요"})
    )

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "placeholder": "이메일을 입력해주세요"}
        ),
    )


class SocialSignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = models.User
        fields = (
            "username",
            "password",
            "email",
            "phone_number",
            "account_name",
            "nickname",
        )

        widgets = {
            "username": forms.HiddenInput,
            "password": forms.HiddenInput,
            "email": forms.HiddenInput,
            "phone_number": forms.HiddenInput,
            "account_name": forms.TextInput(attrs={"placeholder": "이름을 입력하세요"}),
            "nickname": forms.TextInput(attrs={"placeholder": "닉네임을 입력하세요"}),
        }

        labels = {"account_name": "이름", "nickname": "닉네임"}

    def save(self):
        user = models.User.objects.create_user(**self.cleaned_data)

        user.first_name = ""
        user.last_name = ""

        user.save()
