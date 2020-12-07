from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from contactMessages.models import ChatRoom, Message
from django.http import HttpResponseRedirect 
from django.db import IntegrityError
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.views.generic import(
    CreateView,
    ListView
)
from mainApp.models import Pet, Shelter
from .forms import CommentForm
from django.db.models import Count

class BoardMessage(LoginRequiredMixin, ListView):
    template_name = "BoardMessage.html"
    form_model = CommentForm
    Model = Message

    def get_queryset(self):
        return ChatRoom.objects.filter(sender=self.request.user).order_by('-date_created')

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        context['titleTab'] = 'Messages'
        #context['titlePage'] = 'Check your messages'
        
        if self.request.user.is_staff:
            filters = {'shelter': Shelter.objects.get(manager=self.request.user)}
        else:
            filters = {'sender':self.request.user}
        context.update({
            'chatRooms': ChatRoom.objects.filter(**filters).order_by('-date_created')
                        })
        return context

class AnswerMessageAjax(LoginRequiredMixin, CreateView):
    template_name = "BoardMessage.html"
    form_class=CommentForm
    model = Message
     
    def get(self, request, *args, **kwargs):
        message = Message.objects.filter(chatroom__slug=self.kwargs['slug']).order_by('-date_created')
        
        message_serialized = serializers.serialize('json', list(message))
        newMessageUrl = self.request.path_info + "newMessage/"
        return JsonResponse({
            'messages':message_serialized, 
            'user_id': self.request.user.id, 
            'user_sender': message[0].chatroom.sender.username.title(),
            
            'newMessageUrl': newMessageUrl}, status=200)

    def form_valid(self, form): 
        
        chatRoom = ChatRoom.objects.filter(slug=self.kwargs['slug'])
        
        form.instance.sender = self.request.user
        form.instance.chatroom = chatRoom[0]
        form.save()

        return JsonResponse({"message": form.cleaned_data.get('message')}, status=200)
        
    def form_invalid(self, form):
        for m, e in form.errors.as_data().items():
            errorMessage = str(e[0]).replace("['", "").replace("']", "")
        messages.error(self.request, errorMessage)
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CreateMessage(LoginRequiredMixin, CreateView):
    
    form_class=CommentForm
    model = Message

    def form_valid(self, form): 
        pet = Pet.objects.get(slug=self.kwargs['pet'])       
        newChat = ChatRoom.objects.get_or_create(shelter= pet.shelter, sender= self.request.user, pet= pet)
        form.instance.sender = self.request.user
        form.instance.chatroom = newChat[0]
        form.save()
        return JsonResponse({"instance": "Message sent."}, status=200)
        
    def form_invalid(self, form):
        for m, e in form.errors.as_data().items():
            errorMessage = str(e[0]).replace("['", "").replace("']", "")
        messages.error(self.request, errorMessage)
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

        