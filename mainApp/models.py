from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils import timezone
from django.urls import reverse
from django.db import models
from PIL import Image
from django.core.paginator import Paginator

class Shelter(models.Model):
    name = models.CharField(max_length=60, unique=True)
    about = models.TextField(max_length=300)
    location = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank="True")
    manager = models.OneToOneField(User, related_name="usuario", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shelter_imagen", default="default_shelter.jpg")
    date_created = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profile-shelter', kwargs={'slug':self.slug})
    
    def save(self, *args, **kwargs):
       # creates a unique slug
       self.slug = slugify(f"{self.name}")
       super(Shelter, self).save(*args, **kwargs)

    def countPets(self):
        return Pet.objects.filter(shelter=self.id).count()
    
    def Adopted(self):
        return Pet.objects.filter(shelter=self.id, status="Adopted").count()

    def AmountInAdoption(self):
        return Pet.objects.filter(shelter=self.id, status__in=["Urgent","Adoption"]).count()

    def getAllPets(self):
        return Pet.objects.filter(shelter=self.id)

class Pet(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown')
    )
    STATE = (
        ("Adoption", "Adoption"),
        ("Adopted", "Adopted"),
        ("Urgent", "Urgent")
    )
    TYPE = (
        ("Cat", "Cat"),
        ("Dog", "Dog"),
        ("Guinea pig", "Guinea pig"),
        ("Rabbit", "Rabbit"),
        ("Other", "Other")
    )
    COLOR = (
        ("#fbfbfa", "White"),
        ("#000", "Black"),
        ("#800000", "Brown"),
        ("#808080", "Gray"),
    )
    id = models.AutoField(primary_key=True) # this is needed to use the pk in the save method
    name = models.CharField(max_length=60)
    about = models.CharField(max_length=300)
    age = models.PositiveIntegerField(default=0)
    sex = models.CharField(max_length=10, choices=SEX, default="Unknown")
    kind = models.CharField(max_length=10, choices=TYPE, default="Cat")
    weight = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATE, default="Adoption")
    color = models.CharField(max_length=7, choices=COLOR, default="FFF")
    shelter = models.ForeignKey(Shelter, related_name="albergue", default=None, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True) #blank is true but the slug is assigned before saving the pet
    features = models.ManyToManyField("Feature", related_name="pet_atributos_many", blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(f"Adopt {self.name} {get_random_string(length=5)}")
        super(Pet, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pet-detail', kwargs={'slug':self.slug})
    
    def getShelterUrl(self):
        return reverse('shelter-detail', kwargs={'slug':self.slug})

    def petMainPic(self):
        if Images.objects.filter(pet=self, mainPic=True).count() > 0:
            return Images.objects.filter(pet=self, mainPic=True).first().image.url
        return "/media/pet_imagen/default.jpg"

    def petAllPic(self):
        if Images.objects.filter(pet=self).count() > 0:
            return Images.objects.filter(pet=self)
        return ""
    
    def allFeatures(self):
        return Feature.objects.filter(pet=self.id)

    @property
    def thumbnail_preview_list(self):    
        if self.petMainPic:
            try:
                return mark_safe('<img src="{}" width="40px" height="30px" class="img-thumbnail" />'.format(self.petMainPic()))
            except Exception as e :
                pass
        return ""

    def countPets(self):
        return Pet.objects.filter(shelter=self).count()

    def getFilterPets(self, conditions):
        return self.objects.filter(conditions)
    
    def getShelter(self):
        return self.shelter.name

    def getAllFeatures(self):
        return Feature.objects.filter(pet=self)

class Images(models.Model):
    #id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, default="", blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="pet_imagenes")
    image = models.ImageField(upload_to="pet_imagen")
    mainPic = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = get_random_string(length=7)
        if self.mainPic:
            Images.objects.filter(pet=self.pet, mainPic=True).update(mainPic=False)
        super(Images, self).save(*args, **kwargs)
        # img = Image.open(self.image.path)

        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
        # output_size = (450, 450)
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

    def petName(self):
        return self.pet.name
    
    def petSlug(self):
        return self.pet.slug
    
    def get_absolute_url(self):
        return reverse('pet-profile-update', kwargs={'shelter': str(self.pet.shelter.slug), 'pet':self.pet.slug})

class Feature(models.Model):
    # To add things such Vacunated, sick, microchip etc.
    # Like this, everyone could create and delete a feature, and everyone would see all features.
    # Then, only the admin will create, modify and delete them, otherwise, it's going to be annoying to create features
    # every shelter and many will be repeated.
    name = models.CharField(max_length=30, unique=True)
    pet = models.ForeignKey(Pet, related_name="pet_atributo", on_delete=models.CASCADE, blank=True)
    description = models.CharField(max_length=60)

    def __str__(self):
        return self.name
