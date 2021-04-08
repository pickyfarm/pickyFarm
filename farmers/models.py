from django.db import models

class Farmer(models.Model):
    CAT_CHOICES = (
        ("fruit", "과일"),
        ("vege", "채소"),
        ("etc", "기타"),
    )
    farm_name = models.CharField(max_length=50) # 농장 이름
    farmer_profile = models.ImageField(upload_to='farmer_profile/%Y/%m/%d/', null=True, blank=True) # 농장주 사진 default icon 설정
    farm_profile = models.ImageField(upload_to='farm_profile/%Y/%m/%d/') # 농장 대표사진 or 로고
    profile_title = models.CharField(max_length=200) # 농가 한 줄 소개
    profile_desc = models.TextField() # 농가 상세 소개
    sub_count = models.IntegerField(default=0) # 구독자 수
    farm_news = models.CharField(max_length=500, null=True, blank=True) # 농가 뉴스
    farm_cat = models.CharField(choices=CAT_CHOICES, max_length=20, default="fruit")
    open = models.BooleanField(default=False) # 입점 승인 여부
    user = models.OneToOneField(
        'users.User', related_name='farmer', on_delete=models.CASCADE)

    def __str__(self):
        return self.farm_name

    def inc_sub(self):
        self.sub_count += 1
        return


class Farmer_Story(models.Model):
    farmer = models.ForeignKey(
        'Farmer', related_name='farmer_stories', on_delete=models.CASCADE) # 작성자
    title = models.CharField(max_length=50) # 제목
    thumbnail = models.ImageField(upload_to='story_thumbnail/%Y/%m/%d/', null=True, blank=True) # 썸네일
    hits = models.PositiveIntegerField(default=0) # 조회수
    content = models.TextField() # 내용
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.farmer} story - {self.title}'


class Farm_Tag(models.Model):
    tag = models.CharField(max_length=30)
    farmer = models.ManyToManyField(
        "Farmer", related_name='farm_tags')

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
        return f'{self.farm_name}({self.farm_cat}) 입점 신청'
