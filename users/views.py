from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import HttpResponseRedirect, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.views.generic import DeleteView
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.urls import reverse
from django.contrib import messages


from .forms import UserRegisterForm

class MyLoginView(LoginView):
    # Adds functionality to Remember_me in the login
    def form_valid(self, form):
        if not self.request.POST.get('remember_me', None):
            self.request.session.set_expiry(0)
        
        login(self.request, form.get_user())

        return HttpResponseRedirect(self.get_success_url())


class DeleteAccount(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name='users/deleteAccount.html'
    success_url = "/"
    model = User
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Deleting'
        return context

    def test_func(self):
        # Overriden func. Checks that the user is the author
        object = self.get_object()
        if self.request.user == object:
            return True
        return False

class RegisterAccount(FormView):
    template_name='users/createAccount.html'
    #success_url = "/"
    form_class = UserRegisterForm
    model = User

    def get_context_data(self, **kwargs):
        # Calls the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'New account'
        return context

    def get(self, request, *args, **kwargs):
        # The condition has to be checked in get and not get_context_data
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
    
        return super().get(request, *args, **kwargs)


    def form_valid(self, form):
        # Adds the author to the post
        form.instance.author = self.request.user
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            form.save()
            messages.success(self.request, f'Welcome to our community {username}.')
            user = authenticate(
                username = username,
                password = password
            )
            login(self.request, user)
            return super().form_valid(form)
        else:
            for m, e in form.errors.as_data().items():
                errorMessage = str(e[0]).replace("['", "").replace("']", "")

        
        
