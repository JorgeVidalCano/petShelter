from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import CreateMessage, BoardMessage, AnswerMessageAjax

urlpatterns = [
    path('board/', BoardMessage.as_view(), name="board-message"),
    path('board/<slug:slug>/', AnswerMessageAjax.as_view(), name="show-messages"),
    path('board/<slug:slug>/newMessage/', AnswerMessageAjax.as_view(), name="new-message"),
    path('<slug:pet>/newMessage/', CreateMessage.as_view(), name="new_Message"),
]

