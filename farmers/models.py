from django.db import models
from core.models import CompressedImageField
from django.templatetags.static import static
from config.settings import base


class Farmer(models.Model):
    CAT_CHOICES = (
        ("fruit", "과일"),
        ("vege", "채소"),
        ("etc", "기타"),
    )

    COMPANY = (
        ("CJ", "CJ대한통운"),
        ("POST", "우체국택배"),
        ("LOGEN", "로젠택배"),
        ("KG", "KG로지스"),
        ("ILYANG", "일양로지스"),
        ("HYUNDAI", "현대택배"),
        ("GTX", "GTX로지스"),
        ("FedEx", "FedEx"),
        ("HANJIN", "한진택배"),
        ("KYUNG", "경동택배"),
        ("LOTTE", "롯데택배"),
        ("HAPDONG", "합동택배"),
    )
    farm_name = models.CharField(max_length=50)  # 농장 이름
    farmer_profile = CompressedImageField(
        upload_to="farmer_profile/%Y/%m/%d/",
        null=True,
        blank=True,
        default="farmer_default.svg",
    )  # 농장주 사진 default icon 설정
    farm_profile = CompressedImageField(
        upload_to="farm_profile/%Y/%m/%d/",
        null=True,
        blank=True,
        default="farm_default.svg",
    )  # 농장 대표사진 or 로고
    profile_title = models.CharField(max_length=200)  # 농가 한 줄 소개
    farm_desc = CompressedImageField(
        upload_to="farm_desc/%Y/%m/%d/", null=True, blank=True
    )  # 농가 상세 소개
    sub_count = models.IntegerField(default=0)  # 구독자 수
    farm_news = models.CharField(max_length=500, null=True, blank=True)  # 농가 뉴스
    farm_thanks_msg = models.CharField(max_length=500, null=True, blank=True)  # 농가 구매 감사 메세지
    farm_cat = models.CharField(choices=CAT_CHOICES, max_length=20, default="fruit")
    contract = models.BooleanField(default=False)  # 계약서 동의 여부
    open = models.BooleanField(default=False)  # 입점 승인 여부
    user = models.OneToOneField("users.User", related_name="farmer", on_delete=models.CASCADE)
    address = models.OneToOneField(
        "addresses.Address", related_name="farmer", on_delete=models.CASCADE
    )
    delivery_service_company = models.CharField(
        max_length=100, choices=COMPANY, null=True, blank=True, help_text="택배회사"
    )  # 배송 보내는 택배회사
    farm_account = models.CharField(max_length=25, default="계좌번호", help_text="정산 받을 계좌번호")
    shipping_description = models.CharField(max_length=100, default="")  # 배송 기간에 대한 안내

    # 작물 관련법상 표시사항 정보
    law_genetic = models.CharField(max_length=100, default="해당사항 없음")
    law_disease = models.CharField(max_length=100, default="해당사항 없음")
    law_record = models.CharField(max_length=100, default="해당사항 없음")
    law_livestock = models.CharField(max_length=100, default="해당사항 없음")
    law_location = models.CharField(max_length=100, default="해당사항 없음")

    def __str__(self):
        return self.farm_name

    def inc_sub(self):
        self.sub_count += 1
        return


class Farmer_Story(models.Model):
    farmer = models.ForeignKey(
        "Farmer", related_name="farmer_stories", on_delete=models.CASCADE
    )  # 작성자
    title = models.CharField(max_length=50)  # 제목
    thumbnail = CompressedImageField(
        upload_to="story_thumbnail/%Y/%m/%d/", null=True, blank=True, default="mainlogo_small.svg"
    )  # 썸네일
    hits = models.PositiveIntegerField(default=0)  # 조회수
    content = models.TextField()  # 내용
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.farmer} story - {self.title}"


class Farm_Tag(models.Model):
    tag = models.CharField(max_length=30)
    farmer = models.ManyToManyField("Farmer", related_name="farm_tags")

    def __str__(self):
        return self.tag


class Farm_Apply(models.Model):
    CAT_CHOICES = (
        ("fruit", "과일"),
        ("vege", "채소"),
        ("etc", "기타"),
    )
    name = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=30)
    farm_name = models.CharField(max_length=50)
    farm_cat = models.CharField(choices=CAT_CHOICES, max_length=20, default="fruit")
    detail_cat = models.CharField(max_length=50)
    desc = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.farm_name}({self.farm_cat}) 입점 신청"
