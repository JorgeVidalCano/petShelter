from django.contrib import admin
from contactMessages.models import ChatRoom, Message
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    
    list_display = ['shelter', 'sender', 'pet', 'date_created']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'chatroom','message', 'date_created']

    
