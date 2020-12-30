from django.db import models

# Create your models here.

class Comment(models.Model):
    """Comment Model Definition"""

    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    # author = models.ForeignKey("users.User", on_delete=CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Product_Comment(Comment):
    """Product_Comment Model Definition"""

    image = models.ImageField()
    product = models.ForeignKey("products.Product", related_name="product_comments", on_delete=models.CASCADE)

class Product_Recomment(Comment):
    """Product_Recomment Model Definition"""

    comment = models.ForeignKey("Product_Comment", related_name="product_recomments", on_delete=models.CASCADE)


class Qna_Comment(Comment):
    """Qna_Comment Model Definition"""

    qna = models.ForeignKey("products.QnA", related_name="qna_comments", on_delete=models.CASCADE)


class Editor_Review_Comment(Comment):
    """Editor_Review_Comment Model Definition"""

    editor_review = models.ForeignKey("editor_reviews.Editor_Reviews", related_name="editor_review_comments", on_delete=models.CASCADE)

class Editor_Review_Recomment(Comment):
    """Editor_Review_Recomment Model Definition"""

    comment = models.ForeignKey('Editor_Review_Comment', related_name="editor_review_recomments", on_delete=models.CASCADE)
    