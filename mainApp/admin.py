from django.contrib.auth.models import Group
from django.contrib import admin
from .models import Shelter, Pet, Images, Feature
 
admin.site.unregister(Group)

## To add new obj without having to leave the page to create them
class ImageAdmin(admin.StackedInline):
    readonly_fields = ["thumbnail_preview_detail"]
    list_display = ('name', 'thumbnail_preview_list',)
    model = Images

class FeatureAdmin(admin.StackedInline):
    model = Feature

class PetAdmin(admin.StackedInline):
    model = Pet
    inlines = [ImageAdmin, FeatureAdmin]


## To show the models in the admin
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'description']
    ordering = ('name',)

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    inlines = [PetAdmin]
    search_fields = ['name', 'location', 'manager', 'animals']
    list_display = ['name', 'location', 'slug', 'manager', 'animals']
    ordering = ('name', 'location', 'manager')
    
    def animals(self, user):
        return Pet.countPets(user)

    class Meta:
       model = Shelter
 
@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ['name', 'image']
    readonly_fields = ['thumbnail_preview_detail']
    list_display = ['name', 'image', 'thumbnail_preview_list']
    ordering = ('name',)
    
    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Image Preview'
    thumbnail_preview.allow_tags = True


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    search_fields = ['name', 'age', 'sex', 'kind', 'weight', 'visits', 'color', 'shelter', 'date_created']
    readonly_fields = ['visits', 'date_created', 'thumbnail_preview_detail']
    list_display = ['name', 'age', 'sex', 'kind', 'weight', 'visits', 'color', 'shelter', 'date_created', 'thumbnail_preview_list']
    ordering = ('name', 'age', 'sex', 'kind', 'weight', 'visits', 'color', 'shelter', 'date_created')

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Image Preview'
    thumbnail_preview.allow_tags = True