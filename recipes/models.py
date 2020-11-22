import os
import uuid
from io import BytesIO
from django.core.files import File
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.html import mark_safe
from django.utils import timezone
from PIL import Image
from taggit.managers import TaggableManager


def random_filename(instance, filename):
    """
    Returns a random filename to avoid name duplicates when uploading media.
    """

    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("", filename)


def make_thumbnail(image, size=(600, 600)):
    """
    Uses PIL to generate thumbnail.
    Checks for file type and converts it accordingly.
    The image gallery can then use a lightweight thumbnail to
    display the images and renders the full size image only when the
    user clicks on the thumbnail, reducing loading time dramatically.
    """

    im = Image.open(image)
    if im.format == "JPEG":
        im.convert("RGB")
        im.thumbnail(size)
        thumb_io = BytesIO()
        im.save(thumb_io, "JPEG", quality=85)
        thumbnail = File(thumb_io, name=image.name)
    else:
        im.convert("RGBA")
        im.thumbnail(size)
        thumb_io = BytesIO()
        im.save(thumb_io, "PNG", quality=85)
        thumbnail = File(thumb_io, name=image.name)
    return thumbnail


class Recipe(models.Model):
    """Recipe Class"""
    DIFFICULTIES = (
        ('1', 'Easy'),
        ('2', 'Fair'),
        ('3', 'Moderate'),
        ('4', 'Difficult'),
        ('5', 'Expert'),
    )

    name = models.CharField(max_length=254)
    description = models.CharField(max_length=255)
    instructions = models.TextField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES, default=3)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    time = models.IntegerField()
    created = models.DateTimeField(editable=False)
    image = models.ImageField(
        upload_to=random_filename,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["jpeg", "jpg", "png"])],
    )
    thumbnail = models.ImageField(
        upload_to=random_filename, null=True, blank=True
    )
    tags = TaggableManager(blank=True)

    def save(self, *args, **kwargs):
        self.created = timezone.now()
        if self.image:
            self.thumbnail = make_thumbnail(self.image, size=(600, 600))
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    @property
    def thumbnail_preview(self):
        """Admin thumbnail"""

        if self.image:
            return mark_safe(
                '<img src="{}" width="100" height="100" />'.format(
                    self.image.url
                )
            )
        return ""

    def __str__(self):
        return self.name
