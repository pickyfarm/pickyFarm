from django.db import models

# Create your models here.
class Comment(models.Model):
    """Comment Model Definition"""

    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_add= True)
    # author = models.ForeignKey("users.User", on_delete=CASCADE)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.text


class Product_Comment(Comment):
    """Product_Comment Model Definition"""

    image = models.ImageField()
    product = models.ForeignKey("products.Product", on_delete=CASCADE)

# class Consumer_Review_Comment(Comment):
#     """Consumer_Review_Comment Model Definition"""

#     consumer_review = models.ForeignKey("consumer_reviews.Consumer_Review", on_delete=CASCADE)

# class Editor_Review_Comment(Comment):
#     """Editor_Review_Comment Model Definition"""

#     editor_review = models.ForeignKey("editor_reviews.Editor_Reviews", on_delete=CASCADE)


class Recomment(Comment):
    comment = models.ForeignKey("Comment", on_delete=CASCADE)