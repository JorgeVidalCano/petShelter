from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import models
from mainApp.models import Pet, Shelter

class ChatRoom(models.Model):
    shelter = models.ForeignKey(Shelter, related_name="shelter_chatroom", on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(User, related_name="sender_chatroom", on_delete=models.DO_NOTHING)
    pet = models.ForeignKey(Pet, on_delete=models.DO_NOTHING, related_name="pet_chatroom")
    date_created = models.DateField(default=timezone.now)
    
    class Meta:
        unique_together = ["shelter", "sender", "pet"]
    
    def __str__(self):
        return f"{self.shelter.name}-{self.pet.name}-{self.sender.username}"

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

    # def get_absolute_url(self):
    #     return reverse('profile-shelter', kwargs={'slug':self.slug})
    
    # def save(self, *args, **kwargs):
    #    # creates a unique slug
       
    #    super(Shelter, self).save(*args, **kwargs)
