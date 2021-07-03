from django.db import models
from users.models import User
from editor_reviews.models import Editor_Review

# Create your models here.


class AbstractLike(models.Model):
    user = models.ForeignKey("users.User", related_name="Likes", on_delete=models.CASCADE)

    class meta:
        abstract = True


class EditorReviewLike(AbstractLike):
    review = models.ForeignKey(
        "editor_reviews.Editor_Review",
        verbose_name="Editor_Review_Likes",
        related_name="Editor_Review_Likes",
        on_delete=models.CASCADE,
    )


class EditorReviewCommentLike(AbstractLike):
    comment = models.ForeignKey(
        "comments.Editor_Review_Comment",
        verbose_name="Editor_Review_Comment_Likes",
        related_name="editor_review_comment_likes",
        on_delete=models.CASCADE,
    )


class EditorReviewRecommentLike(AbstractLike):
    recomment = models.ForeignKey(
        "comments.Editor_Review_Recomment",
        verbose_name="Editor_Review_Recomment_Likes",
        related_name="editor_review_recomment_likes",
        on_delete=models.CASCADE,
    )


class FarmerStoryCommentLike(AbstractLike):
    comment = models.ForeignKey(
        "comments.Farmer_Story_Comment",
        verbose_name="Farmer_Story_Comment_Likes",
        related_name="Farmer_Story_Comment_Likes",
        on_delete=models.CASCADE,
    )


class FarmerStoryRecommentLike(AbstractLike):
    recomment = models.ForeignKey(
        "comments.Farmer_Story_Recomment",
        verbose_name="Farmer_Story_Recomment_Likes",
        related_name="Farmer_Story_Recomment_Likes",
        on_delete=models.CASCADE,
    )


class ProductRecommentLike(AbstractLike):
    recomment = models.ForeignKey(
        "comments.Product_Recomment",
        verbose_name="Product_Recomment_Likes",
        related_name="Product_Recomment_Likes",
        on_delete=models.CASCADE,
    )
