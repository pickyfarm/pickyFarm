from django.db import models
from io import BytesIO
from django.db.models.fields.files import ImageFieldFile
from django.core.files import File
from PIL import Image, ImageOps
import os

# Create your models here.


class CompressedImageFieldFile(ImageFieldFile):
    def save(self, name, content, save=True):
        # Compressed Image
        image = Image.open(content)
        image = image.convert("RGB")
        image = ImageOps.exif_transpose(image)
        im_io = BytesIO()
        image.save(im_io, "webp", optimize=True)

        # Change extension
        filename = os.path.splitext(name)[0]
        filename = f"{filename}.webp"

        image = File(im_io, name=filename)
        super().save(filename, image, save)


class CompressedImageField(models.ImageField):
    attr_class = CompressedImageFieldFile


class Main_Slider_Image(models.Model):

    image = CompressedImageField(upload_to="main_slider_images/%%Y/%%m/%%d")
    link = models.URLField(max_length=200, default='/product/list')
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)


class NoQuerySet(Exception):
    pass


class AuthorNotMatched(Exception):
    pass
