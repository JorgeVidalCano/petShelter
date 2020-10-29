from django.template.loader import get_template
from carousel.models import Carousel,ImagesCarousel
from django import template

l = get_template('templates/carousel/carousel.html')
obj = ImagesCarousel.objects.all()

## Allows django to load this data everytime without having to repeat the code
register = template.Library()
@register.inclusion_tag(l)
def carousel():
    carouselImgs = obj
    return {
        "carouselImgs": carouselImgs
    }

