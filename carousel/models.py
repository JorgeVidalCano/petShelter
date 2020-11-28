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
            self.name = self.image.url.split("/")[-1]
        super(ImagesCarousel, self).save(*args, **kwargs)
        # img = Image.open(self.image.path)

        # output_size = (1200, 450)
        # img.thumbnail(output_size)
        # img.save(self.image.path)

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
    