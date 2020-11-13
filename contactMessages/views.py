from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from contactMessages.models import ChatRoom, Message
from django.db import IntegrityError
from django.http import HttpResponseRedirect 
from django.shortcuts import render
from django.views.generic import(
    CreateView,
    FormView,
    View
)
from mainApp.models import Pet
from .forms import CommentForm
from django.contrib import messages
from django.http import JsonResponse

from django.core import serializers

class CreateMessage(LoginRequiredMixin, CreateView):
    
    form_class=CommentForm
    model = Message

    def form_valid(self, form): 
        pet = Pet.objects.get(slug=self.kwargs['pet'])       
        try:
            newChat = ChatRoom.objects.create(shelter= pet.shelter, sender= self.request.user, pet= pet)
        except IntegrityError as ex:
            newChat = ChatRoom.objects.get(shelter= pet.shelter, sender= self.request.user, pet= pet)
            # this means the chat already exists
            print("Chat already exists")

        form.instance.sender = self.request.user
        form.instance.receiver = pet.shelter.manager
        form.instance.chatroom = newChat
        form.save()
        return JsonResponse({"instance": "Message sent."}, status=200)
        
    
    def form_invalid(self, form):
        for m, e in form.errors.as_data().items():
            errorMessage = str(e[0]).replace("['", "").replace("']", "")
        messages.error(self.request, errorMessage)
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

        # try:
            # super().post(request, *args, **kwargs)
            # return HttpResponseRedirect(self.get_success_url())
        # except IntegrityError:
            # messages.add_message(request, messages.ERROR, f'Sorry {self.request.user} but only one shelter is allowed per account.')
            # return render(request, template_name=self.template_name, context=self.get_context_data())