from django import forms
from . import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class LoginForm(forms.Form):
    username = forms.CharField(label="아이디", max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요', 'style': 'height:50px'}))
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력해주세요'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = models.User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                raise ValidationError("비밀번호가 틀렸습니다")
        except models.User.DoesNotExist:
            raise ValidationError("존재하지 않는 아이디입니다")


GENDER_CHOICES = {
    ("male", "남자"),
    ("female", "여자"),
}


class SignUpForm(forms.Form):
    username = forms.CharField(label="아이디", max_length=100)
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput)
    password_re = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput)

    last_name = forms.CharField(label="성", max_length=25)
    first_name = forms.CharField(label="이름", max_length=50)

    nickname = forms.CharField(label="닉네임", max_length=100)
    email = forms.EmailField(label="이메일")

    gender = forms.ChoiceField(label="성별", choices=GENDER_CHOICES)
    birth = forms.DateField(widget=forms.SelectDateWidget)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = models.User.objects.get(username=username)
            raise ValidationError("중복된 아이디 입니다. 사용하실 수 없습니다")
        except ObjectDoesNotExist:
            return username

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
        last_name = self.cleaned_data.get("last_name")
        first_name = self.cleaned_data.get("first_name")
        nickname = self.cleaned_data.get("nickname")
        email = self.cleaned_data.get("email")
        gender = self.cleaned_data.get("gender")
        birth = self.cleaned_data.get("birth")

        user = models.User.objects.create_user(username, email=email, password=password_re)

        user.first_name=first_name
        user.last_name=last_name
        user.nickname=nickname
        user.gender=gender
        user.birth=birth

        user.save()
