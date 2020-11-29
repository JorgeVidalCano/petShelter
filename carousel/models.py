from django.utils.crypto import get_random_string
from django.utils.html import mark_safe
from mainApp.models import Image
from django.db import models

class Carousel(models.Model):
    name = models.CharField(max_length=60, default="Carousel")
    
    def __str__(self):
        return self.name

class ImagesCarousel(models.Model):
    
    name = models.CharField(max_length=60, default="", blank=True)
    carousel = models.ForeignKey(Carousel, on_delete=models.CASCADE, related_name="carousel_imagenes")
    image = models.ImageField(upload_to="carousel_imagen")
    
    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = get_random_string(length=9)
        super(ImagesCarousel, self).save(*args, **kwargs)

    @property
    def thumbnail_preview_detail(self):
        return mark_safe('<img src="{}" width="740" height="100%" class="img-thumbnail" />'.format(self.image.url))
        if self.image:
            pass
        return ""
    
    @property
    def thumbnail_preview_list(self):    
        return mark_safe('<img src="{}" width="40px" height="30px" class="img-thumbnail" />'.format(self.image.url))

    def __str__(self):
        return self.name

    def allPics(self):
        return self.objects.all()
    