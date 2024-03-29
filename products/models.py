from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from core.models import CompressedImageField
from django.utils import timezone
from addresses import utils


# Create your models here.


def check_rate(rate_num):
    if rate_num == 1:
        return 2
    elif rate_num == 3:
        return 1
    else:
        return 0


class Product_Group(models.Model):
    kinds = (("ugly", "무난이 작물"), ("normal", "일반 작물"), ("mix", "무난이 + 일반"))

    title = models.CharField(max_length=50, help_text="상품 그룹명")
    sub_title = models.CharField(max_length=100, help_text="상품 그룹 서브명")
    kinds = models.CharField(max_length=100, default="ugly", choices=kinds)

    open = models.BooleanField(default=False, help_text="상품 리스트에 공개 여부")

    main_image = models.ImageField(upload_to="product_main_image/%Y/%m/%d/")
    category = models.ForeignKey(
        "Category", related_name="product_groups", on_delete=models.CASCADE
    )

    sales_rate = models.FloatField(default=0, help_text="상품 전체 판매율")

    total_reviews = models.IntegerField(default=0, help_text="전체 리뷰 수")
    total_avg = models.FloatField(default=0, help_text="상품 전체 평점")

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.open:
            products = self.products.all()
            for product in products:
                product.open = False
                product.status = "suspended"
                product.save()

        super(Product_Group, self).save(*args, **kwargs)  # Call the real save() method

    def get_main_product(self):
        return self.products.get(main_product=True)

    def get_sales_rate(self):
        self.calculate_sales_rate()

        return self.sales_rate

    def calculate_sales_rate(self):
        sales_rate = 0

        for product in self.products.all():
            product.calculate_sale_rate()
            sales_rate += product.sales_rate

        self.sales_rate = sales_rate
        self.save()

    def calculate_total_rating_avg(self):
        total_sum = 0
        total_reviews = 0
        for product in self.products.all():
            total_sum += product.total_rating_sum
            total_reviews += product.reviews
        total_avg = total_sum / total_reviews
        self.total_avg = total_avg
        self.total_reviews = total_reviews
        self.save()

        return self.total_avg

    def calculate_freshness_rating_avg(self):
        [total_freshness_1, total_freshness_3, total_freshness_5] = [0, 0, 0]
        for product in self.products.all():
            total_freshness_1 += product.freshness_1
            total_freshness_3 += product.freshness_3
            total_freshness_5 += product.freshness_5
        freshness_1 = int(100 * total_freshness_1 / self.total_reviews)
        freshness_3 = int(100 * total_freshness_3 / self.total_reviews)
        freshness_5 = int(100 * total_freshness_5 / self.total_reviews)
        return [freshness_1, freshness_3, freshness_5]

    def calculate_flavor_rating_avg(self):
        [total_flavor_1, total_flavor_3, total_flavor_5] = [0, 0, 0]
        for product in self.products.all():
            total_flavor_1 += product.flavor_1
            total_flavor_3 += product.flavor_3
            total_flavor_5 += product.flavor_5
        flavor_1 = int(100 * total_flavor_1 / self.total_reviews)
        flavor_3 = int(100 * total_flavor_3 / self.total_reviews)
        flavor_5 = int(100 * total_flavor_5 / self.total_reviews)
        return [flavor_1, flavor_3, flavor_5]

    def calculate_cost_rating_avg(self):
        [total_cost_1, total_cost_3, total_cost_5] = [0, 0, 0]
        for product in self.products.all():
            total_cost_1 += product.cost_performance_1
            total_cost_3 += product.cost_performance_3
            total_cost_5 += product.cost_performance_5
        cost_1 = int(100 * total_cost_1 / self.total_reviews)
        cost_3 = int(100 * total_cost_3 / self.total_reviews)
        cost_5 = int(100 * total_cost_5 / self.total_reviews)
        return [cost_1, cost_3, cost_5]


class Product(models.Model):
    kinds = (("ugly", "무난이 작물"), ("normal", "일반 작물"), ("mix", "무난이 + 일반"))
    weight_unit = (
        ("g", "g"),
        ("kg", "kg"),
    )

    PRODUCT_STATUS = (
        ("pending", "승인 대기"),
        ("sale", "판매 중"),
        ("suspended", "판매 중지"),
        ("soldout", "품절"),
    )

    title = models.CharField(max_length=50, help_text="상품명")
    sub_title = models.CharField(max_length=100, help_text="상품 서브명")
    main_image = models.ImageField(upload_to="product_main_image/%Y/%m/%d/")

    # option 관련
    option_name = models.CharField(
        max_length=50, null=True, blank=True, help_text="옵션 이름", default="옵션"
    )
    main_product = models.BooleanField(default=False, help_text="상품 그룹에서의 메인 상품 여부")

    kinds = models.CharField(max_length=100, default="ugly", choices=kinds)
    status = models.CharField(max_length=10, choices=PRODUCT_STATUS, default=PRODUCT_STATUS[0][0])
    open = models.BooleanField(default=False)  # to be deleted
    is_event = models.BooleanField(default=False)
    unit_price_desc = models.CharField(max_length=50, null=True, blank=True)

    # 금액 관련
    sell_price = models.IntegerField(default=0, help_text="현재 판매가")
    commision_rate = models.FloatField(default=0, help_text="수수료율")
    discount_price = models.IntegerField(default=0, help_text="할인 금액")
    modify_count = models.IntegerField(default=0, help_text="모델 수정 카운트")

    weight = models.FloatField(help_text="판매 중량")
    weight_unit = models.CharField(max_length=5, choices=weight_unit, help_text="판매 중량 단위")
    stock = models.IntegerField(default=0, help_text="총 재고 수량")
    sales_count = models.IntegerField(default=0, help_text="총 판매 수량", blank=True)
    sales_rate = models.FloatField(default=0, blank=True)

    instruction = models.TextField(blank=True)

    default_delivery_fee = models.IntegerField(default=0, help_text="기본 배송비")
    additional_delivery_fee_unit = models.IntegerField(default=0, help_text="추가 배송비 단위")
    additional_delivery_fee = models.IntegerField(default=0, help_text="추가 배송비")
    jeju_mountain_additional_delivery_fee = models.IntegerField(default=0, help_text="제주/산간 추가 배송비")

    # 반품/교환 배송비
    refund_delivery_fee = models.IntegerField(default=0, help_text="반품 배송비(편도)")
    exchange_delivery_fee = models.IntegerField(default=0, help_text="교환 배송비(왕복)")

    desc_image0 = CompressedImageField(
        upload_to="product_desc_image/%Y/%m/%d/", null=True, blank=True, help_text="긴급 공지용 이미지 영역"
    )
    desc_image = CompressedImageField(
        upload_to="product_desc_image/%Y/%m/%d/", null=True, blank=True
    )
    desc_image2 = CompressedImageField(
        upload_to="product_desc_image/%Y/%m/%d/", null=True, blank=True
    )
    desc_image3 = CompressedImageField(
        upload_to="product_desc_image/%Y/%m/%d/", null=True, blank=True
    )
    desc_image4 = CompressedImageField(
        upload_to="product_desc_image/%Y/%m/%d/", null=True, blank=True
    )
    desc = models.TextField(blank=True)

    # 평점 관련
    reviews = models.IntegerField(default=0)

    total_rating_avg = models.FloatField(default=0)
    total_rating_sum = models.FloatField(default=0)

    freshness_rating_avg = models.FloatField(default=0)
    freshness_rating_sum = models.FloatField(default=0)
    freshness_1 = models.IntegerField(default=0)
    freshness_3 = models.IntegerField(default=0)
    freshness_5 = models.IntegerField(default=0)

    flavor_rating_avg = models.FloatField(default=0)
    flavor_rating_sum = models.FloatField(default=0)
    flavor_1 = models.IntegerField(default=0)
    flavor_3 = models.IntegerField(default=0)
    flavor_5 = models.IntegerField(default=0)

    cost_performance_rating_avg = models.FloatField(default=0)
    cost_performance_rating_sum = models.FloatField(default=0)
    cost_performance_1 = models.IntegerField(default=0)
    cost_performance_3 = models.IntegerField(default=0)
    cost_performance_5 = models.IntegerField(default=0)

    # 상품 상세 정보 관련
    harvest_start_date = models.DateField(
        default=timezone.now, help_text="제조일(수확일) start", null=True
    )
    harvest_end_date = models.DateField(default=timezone.now, help_text="제조일(수확일) end", null=True)
    shelf_life_date = models.CharField(
        max_length=200, blank=True, null=True, help_text="유통기한 또는 품질보증기한"
    )
    storage_method = models.CharField(
        max_length=200, blank=True, null=True, help_text="보관방법 또는 취급방법"
    )

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    related_product = models.OneToOneField(
        "Product", null=True, blank=True, on_delete=models.SET_NULL
    )

    farmer = models.ForeignKey("farmers.Farmer", related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name="products", on_delete=models.CASCADE)
    product_group = models.ForeignKey(
        "Product_Group", related_name="products", on_delete=models.CASCADE, null=True
    )

    def save(self, *args, **kwargs):
        self.weight = round(self.weight, 1)
        self.sales_count = round(self.sales_count, 2)
        self.modify_count += 1
        super(Product, self).save(*args, **kwargs)

    def sold(self, quantity):
        self.stock -= quantity
        self.sales_count += quantity
        if self.stock == 0:
            self.open = False
            self.status = "soldout"
            siblings = self.get_available_sibling_products().exclude(pk=self.pk)
            # 같은 Product_Group 내에 open=True인 상품이 없으면 Product_Group 내리기
            if siblings.count() < 1:
                self.product_group.open = False
            elif siblings.count() >= 1 and self.main_product:
                first = siblings.first()
                self.main_product = False
                first.main_product = True
                first.save()
        self.save()
        return

    def calculate_sale_rate(self):
        rate = self.sales_count / (self.stock + self.sales_count)
        self.sales_rate = rate
        self.save()
        print("판매율 계산")
        return self.sales_rate

    # 할인율 계산 함수 (할인 적용 이후 실행)
    def calculate_discount_rate(self):
        discount_rate = round((self.discount_price / (self.sell_price + self.discount_price)) * 100)
        return discount_rate

    # 리뷰 생성 시 평점 총합 계산을 위한 함수
    def calculate_total_rating_sum(self, new_rating):
        try:
            self.total_rating_sum += new_rating
            self.save()
            return self.total_rating_sum

        except ObjectDoesNotExist:
            return 0

    # 리뷰 생성 시 평점 평균 계산을 위한 함수
    def calculate_total_rating_avg(self):
        try:
            self.total_rating_avg = self.total_rating_sum / self.reviews
            self.save()
            return self.total_rating_avg

        except ObjectDoesNotExist:
            return 0
        except ZeroDivisionError:
            return 0

    # 리뷰 생성 시 항목별 평점(총합, 평균) 계산을 위한 함수
    def calculate_specific_rating(self, fresh, flavor, cost):
        try:
            self.freshness_rating_sum += fresh
            self.flavor_rating_sum += flavor
            self.cost_performance_rating_sum += cost

            self.freshness_rating_avg = self.freshness_rating_sum / self.reviews
            self.flavor_rating_avg = self.flavor_rating_sum / self.reviews
            self.cost_performance_rating_avg = self.cost_performance_rating_sum / self.reviews

            self.save()

        except ObjectDoesNotExist:
            print("specific rating except Object")
            return 0
        except ZeroDivisionError:
            print("specific rating except ZeroDivision")
            return 0
        # freshness_array = [0, 0, 0]
        # flavor_array = [0, 0, 0]
        # cost_performance_array = [0, 0, 0]
        # result = []
        # try:
        #     comments = self.product_comments.all()
        #     if comments.exists() is False:
        #         raise ObjectDoesNotExist
        #     ratio = 100 / comments.count()
        #     for comment in comments:
        #         freshness_array[check_rate(comment.freshness)] += 1
        #         flavor_array[check_rate(comment.flavor)] += 1
        #         cost_performance_array[check_rate(comment.cost_performance)] += 1

        #     for i in range(0, 3):
        #         freshness_array[i] = round(freshness_array[i] * ratio)
        #         flavor_array[i] = round(flavor_array[i] * ratio)
        #         cost_performance_array[i] = round(cost_performance_array[i] * ratio)

        #     result.append(freshness_array)
        #     result.append(flavor_array)
        #     result.append(cost_performance_array)
        #     return result
        # except ObjectDoesNotExist:
        #     result.append(freshness_array)
        #     result.append(flavor_array)
        #     result.append(cost_performance_array)
        #     return result

    def __str__(self):
        return self.title

    def get_sibling_products(self):
        return Product.objects.filter(product_group=self.product_group)

    def get_available_sibling_products(self):
        return self.get_sibling_products().filter(open=True, status="sale")

    def is_sufficient_stock(self, quantity):
        return self.stock >= quantity

    def get_additional_delivery_fee_by_unit(self, quantity):

        """단위별 추가 배송비 계산"""
        """ 기존과 달리 단위별 추가 배송비를 return  """
        try:

            quantity_per_unit = quantity / self.additional_delivery_fee_unit

            print((float)(quantity_per_unit))
            result = 0

            if (float)(quantity_per_unit) >= 1:
                result += (int)(quantity_per_unit) * self.additional_delivery_fee

        except ZeroDivisionError:
            return 0

        return result

    def get_additional_delivery_fee_by_location(self, consumer_zipcode):

        """농가와 소비자의 위치에 따른 배송비 계산"""

        """ 농가가 제주인 경우 : 제주+도서산간에만 추가 배송비
            농가가 제주가 아닌 경우 : 제주+"""

        result = 0
        # consumer_zipcode = int(consumer.default_address.zipcode)
        farm_zipcode = int(self.farmer.address.zipcode)
        is_jeju_mountain = utils.check_address_by_zipcode(consumer_zipcode)

        # # 농가가 제주인 경우
        if 63000 <= farm_zipcode <= 699949:
            # -> 도서산간
            if is_jeju_mountain and consumer_zipcode < 63000:
                result += self.jeju_mountain_additional_delivery_fee
            # -> 그 외
            else:
                result = 0
        # # 그 외
        else:
            # -> 제주 및 도서산간 소비자
            if is_jeju_mountain:
                result += self.jeju_mountain_additional_delivery_fee
            # -> 그 외
            else:
                result = 0

        return result

    def get_total_delivery_fee(self, quantity, consumer_zipcode):

        """전체 배송비 계산"""
        """ 기본배송비 + 단위별 추가 배송비 + 제주산간추가배송비 반환 """

        additional_delivery_fee_by_unit = self.get_additional_delivery_fee_by_unit(quantity)
        additional_delivery_fee_by_location = self.get_additional_delivery_fee_by_location(
            consumer_zipcode
        )

        return (
            self.default_delivery_fee
            + additional_delivery_fee_by_unit
            + additional_delivery_fee_by_location
        )


class Product_Image(models.Model):
    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.CASCADE)

    image = models.ImageField(upload_to="product_images/%Y/%m/%d/")

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        product_name = self.product.title
        return str(product_name + " (" + str(self.pk) + ")")


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey(
        "self", blank=True, null=True, related_name="children", on_delete=models.CASCADE
    )

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return "->".join(full_path[::-1])


class Question(models.Model):
    status = (
        (True, "답변 완료"),
        (False, "답변 대기"),
    )
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = CompressedImageField(upload_to="question_image/%Y/%m/%d/", null=True, blank=True)

    status = models.BooleanField(default=False, choices=status)
    is_read = models.BooleanField(default=False)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    consumer = models.ForeignKey(
        "users.Consumer", related_name="questions", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, related_name="questions", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Answer(models.Model):
    content = models.TextField()
    question = models.OneToOneField(Question, related_name="answer", on_delete=models.CASCADE)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    farmer = models.ForeignKey("farmers.Farmer", on_delete=models.CASCADE)

    def __str__(self):
        return f"'{self.question}' 에 대한 답변"


def get_delete_product():
    return Product.objects.get_or_create(title="삭제된 상품")[0]
