from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from contactMessages.models import ChatRoom, Message
from django.http import HttpResponseRedirect 
from django.shortcuts import render
from django.views.generic import(
    CreateView
)
from .forms import CommentForm
from django.contrib import messages

class CreateMessage(LoginRequiredMixin, CreateView):
    model = Message
    form_class=CommentForm

    def form_valid(self, form):
        # Adds the author to the post
        form.instance.manager = self.request.user
        
        # only access if some pic is uploaded
        if bool(self.request.FILES):
            form.instance.image = self.request.FILES['image']
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for m, e in form.errors.as_data().items():
            errorMessage = str(e[0]).replace("['", "").replace("']", "")
        messages.error(self.request, errorMessage)
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        # try:
            # super().post(request, *args, **kwargs)
            # return HttpResponseRedirect(self.get_success_url())
        # except IntegrityError:
            # messages.add_message(request, messages.ERROR, f'Sorry {self.request.user} but only one shelter is allowed per account.')
            # return render(request, template_name=self.template_name, context=self.get_context_data())