from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from mainApp.models import Pet, Shelter
from django.utils import timezone
from django.urls import reverse
from django.db import models

class ChatRoom(models.Model):
    shelter = models.ForeignKey(Shelter, related_name="shelter_chatroom", on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(User, related_name="sender_chatroom", on_delete=models.DO_NOTHING)
    pet = models.ForeignKey(Pet, on_delete=models.DO_NOTHING, related_name="pet_chatroom")
    slug = models.SlugField(unique=True, blank="True")
    date_created = models.DateField(default=timezone.now)
    
    class Meta:
        unique_together = ["shelter", "sender", "pet"]
    
    def __str__(self):
        return f"{self.shelter.name}-{self.pet.name}-{self.sender.username}"
    
    def save(self, *args, **kwargs):
       # creates a unique slug
       self.slug = get_random_string(length=7)
       super(ChatRoom, self).save(*args, **kwargs)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender_comment", on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(User, related_name="manager_comment", on_delete=models.DO_NOTHING)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="chatroom_Message")
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.message[:40]

    def get_success_url(self):
        return reverse('detail-pet', kwargs={'slug':self.pet})
