from django.db import models
from products.models import Product, Category
from users.models import Editor


# Create your models here.

class Editor_Reviews(models.Model):

    title = models.TextField()
    main_image = models.ImageField(upload_to='editor_review_thumbnail/%%Y/%%m/%%d')
    contents = models.TextField()
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    #author = models.ForeignKey(Editor, related_name="editor_reviews", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="editor_reviews", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="editor_reviews", on_delete=models.CASCADE)

    def get_preview(self):
        if len(self.contents) < 60:
            return self.contents

        else:
            return self.contents[:60]
    
    # def review_count(self):
    #     return Editor_Reviews.objects.filter(author=self.author.user.nickname).count()



class Editor_Reviews_Image(models.Model):

    image = models.ImageField(upload_to='editor_review_images')
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Editor_Reviews, related_name="editor_review_images", on_delete=models.CASCADE)