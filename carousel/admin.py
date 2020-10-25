from django.contrib import admin
from .models import Carousel, ImagesCarousel

class InlineImageAdmin(admin.StackedInline):
    model = ImagesCarousel
    extra = 3
    max_num = 3

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    inlines = [InlineImageAdmin]
    # list_display = ("images")

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    def has_add_permission(self, request, obj=None):
        # The add button disapear when there is one carousel
        if Carousel.objects.all().count() == 1:
            return False
        else:
            return True

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True
