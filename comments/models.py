from django.db import models
from users.models import User


# Create your models here.


class Comment(models.Model):
    """Comment Model Definition"""

    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # author = models.ForeignKey("users.User", on_delete=CASCADE)
    

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Product_Comment(Comment):
    """Product_Comment Model Definition"""
    
    evaluate = (
        (5, 'good'),
        (3, 'normal'),
        (1, 'bad'),
    )

    freshness = models.IntegerField(choices=evaluate)
    flavor = models.IntegerField(choices=evaluate)
    cost_performance = models.IntegerField(choices=evaluate)
    avg = models.IntegerField(default = 0)
    
    product = models.ForeignKey("products.Product", related_name="product_comments", on_delete=models.CASCADE)
    consumer = models.ForeignKey("users.Consumer", related_name="product_comments", on_delete=models.CASCADE)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def get_rating_avg(self): 
        self.avg = round((self.freshness+self.flavor+self.cost_performance)/3)
        return self.avg
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.get_rating_avg()
        print(self.avg)
        super(Product_Comment, self).save(*args, **kwargs)


class Product_Comment_Image(models.Model):

    image = models.ImageField(upload_to="comments/%Y/%m/%d/")
    product_comment = models.ForeignKey(Product_Comment, related_name="product_comment_images", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_comment.product.title} : {self.product_comment.text} - 상품 리뷰 사진'



class Product_Recomment(Comment):
    """Product_Recomment Model Definition"""

    comment = models.ForeignKey("Product_Comment", related_name="product_recomments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='product_recomment', on_delete=models.CASCADE)

# class Qna_Comment(Comment):
#     """Qna_Comment Model Definition"""

#     qna = models.ForeignKey("products.QnA", related_name="qna_comments", on_delete=models.CASCADE)


class Editor_Review_Comment(Comment):
    """Editor_Review_Comment Model Definition"""

    editor_review = models.ForeignKey("editor_reviews.Editor_Review", related_name="editor_review_comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='editor_review_comment', on_delete=models.CASCADE)


class Editor_Review_Recomment(Comment):
    """Editor_Review_Recomment Model Definition"""

    comment = models.ForeignKey('Editor_Review_Comment', related_name="editor_review_recomments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='editor_review_recomment', on_delete=models.CASCADE)


class Farmer_Story_Comment(Comment):
    """Farmer_Story_Comment Model Defiition"""

    story = models.ForeignKey("users.Farmer_Story", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='farmer_story_comments', on_delete=models.CASCADE)


class Farmer_Story_Recomment(Comment):
    """Farmer_Story_Recomment Model Defiition"""

    comment = models.ForeignKey("Farmer_Story_Comment", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='farmer_story_recomments', on_delete=models.CASCADE)