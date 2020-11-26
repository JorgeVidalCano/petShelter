from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# from users.forms import UserUpdateForm
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import(
     ListView, 
     DetailView, 
     CreateView,
     UpdateView,
     DeleteView,
     TemplateView
    )
from .forms import ShelterForm, PetForm, ImageForm
from .models import Pet, Shelter, Feature, Images
from django.core.paginator import Paginator
from django.http import JsonResponse
from contactMessages.forms import CommentForm
import copy
import json
from searchEngine.forms import petSearchForm
ROWPET = 3 # Const. amount of pets per row

class HomeView(TemplateView):
    template_name = "mainApp/home.html"
    model = Pet
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        filters = {"status__in":["Urgent","Adoption"]}
        
        context.update({
            'titleTab': 'Home',
            'pets': Pet.objects.filter(**filters).order_by("?")[:ROWPET],
            'form': petSearchForm()
        })
        shelters = Shelter.objects.order_by("?")[:2]
        # list of pets in shelters
        if shelters.count() > 1:            
            # shelters are a refval so it keeps changing. A copy it's needed to keep the order
            shelterCopy=copy.copy(shelters)

            context.update({
                'pets': Pet.objects.filter(**filters).order_by("?")[:ROWPET],
                'shelterName1': shelterCopy[0],
                'shelterName2': shelterCopy[1],
                'shelter': shelterCopy[0],
                'petShelter1': Pet.objects.filter(**filters)[:ROWPET],
                'slugShelter1': shelterCopy[0], # needed to get the url
                'shelter': shelterCopy[1],
                'petShelter2': Pet.objects.filter(**filters)[:ROWPET],
                'slugShelter2':shelterCopy[1]
            })

        return context

class DetailPetView(DetailView):
    template_name = "mainApp/detail_pet.html"
    model = Pet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titleTab'] = f"{kwargs['object']} details"
        filters = {
            "kind": kwargs['object'].kind,
            "status__in": ["Urgent","Adoption"],
            "age__gte": kwargs['object'].age - 2,
            "age__lte": kwargs['object'].age + 2,
        }
        excludes = {"id": kwargs['object'].id}
        context['related_pets'] = Pet.objects.filter(**filters).exclude(**excludes).order_by("?")[:ROWPET]
        # if we get less than 4 related pets, with do a less restrictive query
        if context['related_pets'].count() < 4:
            context['related_pets'] = Pet.objects.filter(kind= kwargs['object'].kind, status__in= ["Urgent","Adoption"],).exclude(**excludes).order_by("?")[:ROWPET]

        form = CommentForm()
        context.update({"comment":form})

        return context

class PetsView(ListView):
    template_name = "mainApp/pets.html"
    model = Pet

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        petsCopy = Pet.objects.filter().order_by("?")[:ROWPET+5]

        context.update({
            'titleTab': 'Pets',
            'title': 'Pets',
            'PetList': petsCopy,
            'shelterId': [s.id for s in petsCopy] # we pass it so the lazy Search doesnt repeat
        })
        return context

class ShelterView(TemplateView):
    template_name = "mainApp/shelters.html"
    model = Shelter

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        shelterCopy = Shelter.objects.filter().order_by("?")[:ROWPET+1]

        context.update({
            'titleTab': 'Shelters',
            'title': 'Shelters',
            'shelter': shelterCopy,
            'shelterId': [s.id for s in shelterCopy] # we pass it so the lazy Search doesnt repeat
        })
        return context

class DetailShelterView(DetailView):
    template_name = "mainApp/detail_shelter.html"
    model = Shelter

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = f"{kwargs['object']} details"

        context['AmountInAdoption'] =  kwargs['object'].AmountInAdoption()
        context['total'] = kwargs['object'].countPets()

        context['pets'] = Pet.objects.filter(shelter=kwargs['object']).order_by('-date_created')[:ROWPET]

        return context

class BaseProfileView (LoginRequiredMixin, TemplateView):
    template_name = "profile/profileSummarize.html"
    model = Shelter
    
    def get(self, request, *args, **kwargs):
        shelter = Shelter.objects.filter(manager=self.request.user)
        if shelter.count() == 0:
            return HttpResponseRedirect(reverse('shelter-new'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        shelter = Shelter.objects.get(manager= self.request.user)
        context['titleTab'] = f'Your {shelter.name}'
        context['object'] = shelter
        return context

class CreateShelterView(LoginRequiredMixin, CreateView):
    template_name = "forms/shelter.html"
    form_class = ShelterForm
    model = Shelter
    
    def get(self, request, *args, **kwargs):
        shelter = Shelter.objects.filter(manager=self.request.user)
        if shelter.count() > 0:
            return HttpResponseRedirect(reverse('profile-shelter', kwargs={'slug':Shelter.objects.get(manager=self.request.user).slug}))
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        context['titleTab'] = 'Create New shelter'
        context['titleFormShelter'] = "Create New Adoption Shelter"
        context['paragraph'] = 'Fill the required info for your shelter'
        return context
    
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
        try:
            super().post(request, *args, **kwargs)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            messages.add_message(request, messages.ERROR, f'Sorry {self.request.user} but only one shelter is allowed per account.')
            return render(request, template_name=self.template_name, context=self.get_context_data())
    
    def test_func(self):
        # Check that the user is the manager
        shelter = self.get_object()
        if self.request.user == shelter.manager:
            return True
        return False

class UpdateShelterView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "profile/profile_shelter.html"
    form_class = ShelterForm
    model = Shelter
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = context['object'].name
        context['titleFormShelter'] = context['object'].name
        return context

    def form_invalid(self, form):
        for m, e in form.errors.as_data().items():
            errorMessage = str(e[0]).replace("['", "").replace("']", "")
        messages.error(self.request, errorMessage)
        return super().form_invalid(form) 

    def test_func(self):
        # Checks that the user is the manager
        shelter = self.get_object()
        if self.request.user == shelter.manager:
            return True
        return False

class DeleteShelterView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "forms/shelter_confirm_delete.html"
    model = Shelter
    success_url = "/"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Deleting your shelter'
        return context

    def test_func(self):
        # Checks that the user is the manager
        shelter = self.get_object()
        if self.request.user == shelter.manager:
            return True
        return False

class ListPetsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "profile/listPets.html"
    ordering = ['date_created']
    form_model = PetForm
    Model = Shelter

    def get_queryset(self):
        ordering = ['date_created']
        return Pet.objects.filter(shelter__slug=self.request.user).order_by('-date_created')

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        context['titleTab'] = 'Pets'
        context['titlePage'] = 'All Pets in your shelter'
        context['object'] = Shelter.objects.get(manager= self.request.user)
        context['pets'] = context['object'].getAllPets()
        return context
    
    def test_func(self):
        # Checks that the user is the manager
        manager = Shelter.objects.get(slug=self.kwargs['shelter']).manager
        if self.request.user == manager:
            return True
        return False

class CreatePetProfileView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    template_name = "profile/create_pet.html"
    form_class = PetForm
    model = Pet

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        context['titleTab'] = "New pet"
        context['titleFormShelter'] = "New pet"
        context['object'] = Shelter.objects.get(manager= self.request.user)
        # context['buttonName'] = 'Update {petName}'
        
        context['petImages'] = ''
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.shelter= Shelter.objects.get(manager=self.request.user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for m, e in form.errors.as_data().items():
            errorMessage = str(e[0]).replace("['", "").replace("']", "")
        messages.error(self.request, errorMessage)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('pet-image-new', kwargs={'pet': str(self.object.slug)})
    
    def test_func(self):
        # Checks that the user is the manager
        manager = Shelter.objects.get(slug=self.kwargs['shelter']).manager
        if self.request.user == manager:
            return True
        return False

class UpdatePetProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "profile/profile_pet.html"
    form_class = PetForm
    model = Pet
    
    def get_object(self, queryset=None):
        #https://stackoverflow.com/questions/57614381/generic-detail-view-postdetailview-must-be-called-with-either-an-object-pk-or-a
        # Since I'm using 2 variables in the url, django
        # doesn't know how to use the second one.
        if queryset is None:
            queryset = self.get_queryset()
        new_str = self.kwargs.get('pet') or self.request.GET.get('pet') or None

        queryset = queryset.filter(slug=new_str)
        obj = queryset.get()
        return obj

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        petName = context['object'].name.title()
        context['titleTab'] = f'{petName} pet'
        context['petSlug'] = context['object']
        context['object'] = Shelter.objects.get(manager= self.request.user)
        context['buttonName'] = f'Update {petName}'
        context['titleFormShelter'] = self.object.name.title
        context['petImages'] = Images.objects.filter(pet=self.object)
        return context

    def get_success_url(self):
        return reverse('pet-profile-update', kwargs={'shelter': str(Shelter.objects.get(manager= self.request.user).slug), 'pet':str(self.object.slug)})
    
    def form_invalid(self, form):
        for m, e in form.errors.as_data().items():
            errorMessage = str(e[0]).replace("['", "").replace("']", "")
        messages.error(self.request, errorMessage)
        return super().form_invalid(form)
    

    def test_func(self):
        # Check that the user is the manager
        pet = self.get_object()
        if self.request.user == pet.shelter.manager:
            return True
        return False

class DeletePetProfileView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "forms/pet_confirm_delete.html"
    form_class = PetForm
    model = Pet

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        context['titleTab'] = f'Delete {self.object.name.title()}'
        context['titleH1'] = f'Delete {self.object.name.title()}'
        context['petImg'] = Images.objects.get(pet=self.object, mainPic=True)
        context['object'] = Shelter.objects.get(manager= self.request.user)
        
        return context

    def get_success_url(self):
        return reverse_lazy('pets', kwargs={'shelter': str(Shelter.objects.get(manager= self.request.user).slug)})
    
    def test_func(self):
        # Check that the user is the manager
        pet = self.get_object()
        if self.request.user == pet.shelter.manager:
            return True
        return False

class CreateImageView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "profile/createImagen.html"
    form_class = ImageForm
    model = Images

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        context['titleTab'] = 'New imagen'
        context['object'] = Shelter.objects.get(manager= self.request.user)
        context['buttonName'] = 'New imagen'
        context['titleH1'] = Pet.objects.get(slug=self.kwargs['pet']).name
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            form.instance.pet=Pet.objects.get(slug=self.kwargs['pet'])
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for m, e in form.errors.as_data().items():
            errorMessage = str(e[0]).replace("['", "").replace("']", "")
        messages.error(self.request, errorMessage)
        return super().form_invalid(form)
    
    def test_func(self):
        # Checks that the user is the manager
        manager = Pet.objects.get(slug=self.kwargs['pet']).shelter
        if self.request.user == manager.manager:
            return True
        return False

class UpdateImageView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "profile/updateImagen.html"
    context_object_name = 'petImg'
    form_class = ImageForm
    model = Images

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        context['titleTab'] = 'Update imagen'
        context['object'] = Shelter.objects.get(manager= self.request.user)
        context['buttonName'] = 'Update imagen'
        context['titleH1'] = Images.objects.get(pk=self.kwargs['pk']).pet.name
        return context

    def form_invalid(self, form):
        for m, e in form.errors.as_data().items():
            errorMessage = str(e[0]).replace("['", "").replace("']", "")
        messages.error(self.request, errorMessage)
        return super().form_invalid(form)
    
    def test_func(self):
        # Checks that the user is the manager
        pet = Images.objects.get(pk=self.kwargs['pk']).pet
        if self.request.user == pet.shelter.manager:
            return True
        return False

class DeleteImageView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "forms/image_confirm_delete.html"
    context_object_name = 'petImg'
    form_class = ImageForm
    model = Images

    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Update imagen'
        context['object'] = Shelter.objects.get(manager= self.request.user)
        context['buttonName'] = 'Update imagen'
        context['titleH1'] = Images.objects.get(pk=self.kwargs['pk']).pet.name
        return context

    def get_success_url(self):
        return reverse('pet-profile-update', kwargs={'shelter': str(Shelter.objects.get(manager= self.request.user).slug), 'pet':str(Images.objects.get(pk=self.kwargs['pk']).pet.slug)})
    
    def test_func(self):
        # Checks that the user is the manager
        pet = Images.objects.get(pk=self.kwargs['pk']).pet
        if self.request.user == pet.shelter.manager:
            return True
        return False

class LazyReload(ListView):

    def get(self, request, *args, **kwargs):
        
        if self.request.is_ajax() and self.request.method == "GET":

            filters = {
                "status__in":["Urgent","Adoption"]
            }
            try:
                self.pet_list = Pet.objects.filter(**filters).order_by("?")
                self.page = self.selectPetsByPage(self.pet_list)
                ser_instance = self.getPets(self.page)                
                return JsonResponse({"instance": ser_instance, "end": False}, status=200)
            except Exception as ex:
                print(ex)
                return JsonResponse({"instance": None, "end": True}, status=200)    
    
    def selectPetsByPage(self, pet_list):
        # we select the next 5 pets
        numberPage = self.kwargs.get("page")

        splitPag = Paginator(self.pet_list, round(self.pet_list.count()/5))
        self.page = splitPag.page(numberPage)
        
        return self.page
    
    def getPets(self, page_pet):
        # we get the 5 pets and serialize them
        pets = self.preserializer(page_pet)
        ser_instance = json.dumps(list(pets))
        
        return ser_instance

    def preserializer(self, page_pet):
        # the queryset and create a dict and add it to a list
        pets = []
        pet = {}

        for p in page_pet.object_list:
            pet = {
                "name": p.name.title(),
                "sex": p.sex,
                "status": p.status,
                "shelter": p.shelter.name.title(), 
                "images": p.petMainPic(),
                "slug" : f"pet/{p.slug}",
                "date_created": p.date_created.strftime("%b %d, %Y"),
            }
            pets.append(pet)
        return pets

class LazyReloadShelters(ListView):
    def get(self, request, *args, **kwargs):
        
        if self.request.is_ajax() and self.request.method == "GET":
            
            try:
                filters={
                    "id__in": self.request.GET['idShelter'].replace("[", "").replace("]", "").split(",")
                }
                self.shelter_list = Shelter.objects.all().exclude(**filters).order_by("?")
                self.page = self.selectShelterPage(self.shelter_list)
                ser_instance = self.getShelter(self.page)
                return JsonResponse({"instance": ser_instance, "end": False}, status=200)
            except Exception as ex:
                print(ex)
                return JsonResponse({"instance": None, "end": True}, status=200)    
    
    def selectShelterPage(self, shelter_list):
        # we select the next 5 shelters
        numberPage = self.kwargs.get("page")

        splitPag = Paginator(self.shelter_list, round(self.shelter_list.count()/5))
        self.page = splitPag.page(numberPage)
        
        return self.page
    
    def getShelter(self, page_shelter):
        # we get the 5 shelter and serialize them
        shelters = self.preserializer(page_shelter)
        ser_instance = json.dumps(list(shelters))
        
        return ser_instance

    def preserializer(self, page_shelter):
        # the queryset and create a dict and add it to a list
        shelters = []
        shelter = {}
        for p in page_shelter.object_list:
            
            shelter = {
                "name": p.name.title(),
                "about": p.about,
                "location": p.location,
                "image": p.image.url,
                "petAdoption": p.AmountInAdoption(),
                "slug" : f"{p.slug}",
            }
            shelters.append(shelter)
        return shelters

# class ProfileOptionsShelter(LoginRequiredMixin, UpdateView):
#     template_name = "profile/profileOptions.html"
#     form_class = UserUpdateForm
#     model = User
    
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super().get_context_data(**kwargs)
#         context['titleTab'] = 'Options'
#         #context['object'] = Shelter.objects.get(manager= self.request.user)
        
#         return context