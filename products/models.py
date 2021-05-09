from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


def check_rate(rate_num):
    if rate_num == 1:
        return 2
    elif rate_num == 3:
        return 1
    else:
        return 0


class Product(models.Model):
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to="product_main_image/%Y/%m/%d/")
    open = models.BooleanField(default=False)

    sell_price = models.IntegerField(default=0, help_text="현재 판매가")
    weight = models.FloatField()
    stock = models.IntegerField(default=0, help_text="총 재고 수량")
    sales_count = models.IntegerField(default=0, help_text="총 판매 수량", blank=True)
    sales_rate = models.FloatField(default=0, blank=True)

    instruction = models.TextField(blank=True)

    desc_image = models.ImageField(upload_to="product_desc_image/%Y/%m/%d/", null=True, blank=True)
    desc = models.TextField(blank=True)

    # 평점 관련
    reviews = models.IntegerField(default=0)

    total_rating_avg = models.FloatField(default=0)
    total_rating_sum = models.FloatField(default=0)

    freshness_rating_avg = models.FloatField(default=0)
    freshness_rating_sum = models.FloatField(default=0)

    flavor_rating_avg = models.FloatField(default=0)
    flavor_rating_sum = models.FloatField(default=0)

    cost_performance_rating_avg = models.FloatField(default=0)
    cost_performance_rating_sum = models.FloatField(default=0)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    farmer = models.ForeignKey("farmers.Farmer", related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name="products", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.weight = round(self.weight, 1)
        self.sales_count = round(self.sales_count, 2)
        super(Product, self).save(*args, **kwargs)

    def sold(self):
        if self.stock > 0:
            self.stock -= 1
            self.sales_count += 1
            self.save()
        else:
            self.open = False
            self.save()
        return

    def calculate_sale_rate(self):
        rate = self.sales_count / (self.stock + self.sales_count)
        self.sales_rate = rate
        self.save()
        print("판매율 계산")
        return self.sales_rate

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


class Product_Image(models.Model):
    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.CASCADE)

    image = models.ImageField(upload_to="product_images/%Y/%m/%d/")

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


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
    image = models.ImageField(upload_to="question_image/%Y/%m/%d/", null=True, blank=True)

    status = models.BooleanField(default=False, choices=status)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    consumer = models.ForeignKey(
        "users.Consumer", related_name="questions", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, related_name="questions", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    question = models.OneToOneField(Question, related_name="answer", on_delete=models.CASCADE)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    farmer = models.ForeignKey("farmers.Farmer", on_delete=models.CASCADE)

    def __str__(self):
        return self.question.__str__().join("에 대한 답변")


def get_delete_product():
    return Product.objects.get_or_create(title="삭제된 상품")[0]
