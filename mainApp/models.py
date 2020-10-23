from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils import timezone
from django.urls import reverse
from django.db import models

class Shelter(models.Model):
    name = models.CharField(max_length=60, unique=True)
    location = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank="True")
    manager = models.ForeignKey(User, related_name="usuario", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # creates a unique slug
        self.slug = slugify(f"{self.name}")
        super(Shelter, self).save(*args, **kwargs)

    def countPets(self):
        return Pet.objects.get(Shelter=self.name).count()
    
    def get_absolute_url(self):
        return reverse('shelter-detail', kwargs={'slug':self.slug})

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
        ("Other", "Other")
    )
    COLOR = (
        ("#fbfbfa", "White"),
        ("000", "Black"),
        ("#800000", "Brown"),
        ("#808080", "Gray"),
    )
    id = models.AutoField(primary_key=True) # this is need to use the pk in the save method
    name = models.CharField(max_length=60)
    about = models.CharField(max_length=300)
    age = models.PositiveIntegerField(default=0)
    sex = models.CharField(max_length=10, choices=SEX, default="Unknown")
    kind = models.CharField(max_length=5, choices=TYPE, default="Cat")
    weight = models.PositiveIntegerField(default=0)
    visits = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATE, default="Adoption")
    color = models.CharField(max_length=7, choices=COLOR, default="FFF")
    shelter = models.ForeignKey(Shelter, related_name="albergue", default=None, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True) #blank is true but is changed before saving the pet

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # creates a unique slug
        self.slug = slugify(f"Adopt {self.name} {self.id}")
        super(Pet, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pet-detail', kwargs={'slug':self.slug})

    def petMainPic(self):
        return Images.objects.filter(pk = self.pk).first().image.url

    def petAllPics(self):
        #return Images.objects.filter(pk = self.pk).image.url
        return self.related.all()#.images#.values("images")
 
    @property
    def thumbnail_preview_list(self):    
        if self.petMainPic:
            try:
                print(self.petMainPic())
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

class Images(models.Model):
    
    name = models.CharField(max_length=60, default="", blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="pet_imagenes")
    image = models.ImageField(upload_to="pet_imagen")

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = self.image.url.split("/")[-1]
        super(Images, self).save(*args, **kwargs)

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
    
    def firstPic(self):
        return self.objects.first()
    
    def petName(self):
        return self.pet.name

class Feature(models.Model):
    # To add things such Vacunated, sick, microchip etc.
    # Like this, everyone could create and delete a feature, and everyone would see all features.
    # Then, only the admin will create, modify and delete them, otherwise, it's going to be annoying to create features
    # every shelter and many will be repeated.
    name = models.CharField(max_length=30, unique=True)
    pet = models.ForeignKey(Pet, related_name="pet_atributos", on_delete=models.CASCADE, blank=True)
    description = models.CharField(max_length=60)

    def __str__(self):
        return self.name

