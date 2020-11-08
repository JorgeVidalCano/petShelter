from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate
from django.shortcuts import HttpResponseRedirect, redirect
from django.views.generic import DeleteView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse

from .forms import UserRegisterForm

class MyLoginView(LoginView):
    # Adds functionality to Remember_me in the login
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        if not self.request.POST.get('remember_me', None):
            self.request.session.set_expiry(0)
        
        login(self.request, form.get_user())

        return HttpResponseRedirect(self.get_success_url())


class DeleteAccount(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name='users/deleteAccount.html'
    success_url = "/"
    
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

class DeleteAccount(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name='users/deleteAccount.html'
    success_url = "/"
    
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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, label_suffix='')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()
            messages.success(request, f'Welcome to our community {username}.')
            user = authenticate(
                username = username,
                password = password
            )
            login(request, user)
            return redirect('blog-home')
        else:
            for m, e in form.errors.as_data().items():
                errorMessage = str(e[0]).replace("['", "").replace("']", "")
            messages.error(request, errorMessage)
    else:
        form = UserRegisterForm(label_suffix='')
    if request.user.is_authenticated:
        return redirect('profile')
        
    context = {
        "form": form,
        "titleTab": "Profile",
    }
    return render(request, 'users/register.html', context)
