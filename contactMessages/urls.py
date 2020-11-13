from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import CreateMessage

urlpatterns = [
    path('<slug:pet>/newMessage/', CreateMessage.as_view(), name="new_Message"),
]

