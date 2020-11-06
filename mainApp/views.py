from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from users.forms import UserUpdateForm
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
from django.core.paginator import Paginator
from .forms import ShelterForm, PetForm#, featureFormInline
from django.http import JsonResponse
from .models import Pet, Shelter, Feature, Images
import copy
import json

ROWPET = 3 # Const. amount of pets per row

class HomeView(TemplateView):
    template_name = "mainApp/home.html"
    model = Pet
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Home'
        
        filters = {"status__in":["Urgent","Adoption"]}
        
        context['pets'] = Pet.objects.filter(**filters).order_by("?")[:ROWPET] # all pets
        shelters = Shelter.objects.order_by("?")[:2]
        
        # list of pets in shelters
        if shelters.count() > 1:            
            # shelters are a refval so it keeps changing. A copy it's needed to keep order
            shelterCopy=copy.copy(shelters)
            context['shelterName1'] = shelterCopy[0]
            context['shelterName2'] = shelterCopy[1]

            filters["shelter"] = shelterCopy[0]
            context['petShelter1'] = Pet.objects.filter(**filters)[:ROWPET]
            context['slugShelter1'] = shelterCopy[0] # needed to get the url


            filters["shelter"] = shelterCopy[1]
            context['petShelter2'] = Pet.objects.filter(**filters)[:ROWPET]
            context['slugShelter2'] = shelterCopy[1]

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


        return context

class ShelterView(TemplateView):
    template_name = "mainApp/shelters.html"
    model = Shelter

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Shelters'

        context['shelter'] = Shelter.objects.filter().order_by("?")[:ROWPET]

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

class CreateShelterView(LoginRequiredMixin, CreateView):
    #permision_required = ""
    template_name = "forms/shelter.html"
    form_class = ShelterForm
    model = Shelter
    
    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        context['titleTab'] = 'Create New shelter'
        context['titleFormShelter'] = "Adoption Shelter"
        context['paragraph'] = 'Fill the required info for your shelter'
        return context
    
    def form_valid(self, form):
        # Adds the author to the post
        form.instance.manager = self.request.user
        
        # only access if some pic is uploaded
        if bool(self.request.FILES):
            form.instance.image = self.request.FILES['image']
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        try:
            super().post(request, *args, **kwargs)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            messages.add_message(request, messages.ERROR, f'Sorry {self.request.user} but only one shelter is allowed per account.')
            return render(request, template_name=self.template_name, context=self.get_context_data())
    
class UpdateShelterView(LoginRequiredMixin, UpdateView):
    #permision_required = ""
    template_name = "profile/profile_shelter.html"
    form_class = ShelterForm
    model = Shelter
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = context['object'].name
        context['titleFormShelter'] = context['object'].name
        return context
        
class ProfileOptionsShelter(LoginRequiredMixin, UpdateView):
    template_name = "profile/profileOptions.html"
    form_class = UserUpdateForm
    model = User
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Options'
        #context['object'] = Shelter.objects.get(manager= self.request.user)
        
        return context

class DeleteShelterView(LoginRequiredMixin, DeleteView):
    template_name = "forms/shelter_confirm_delete.html"
    model = Shelter
    success_url = "/"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Deleting your shelter'
        return context

    def test_func(self):
        # Overriden func. Checks that the user is the author
        shelter = self.get_object()
        if self.request.user == shelter.manager:
            return True
        return False

class ListPetsView(LoginRequiredMixin, ListView):
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

class CreatePetProfileView(LoginRequiredMixin, CreateView):
    pass

from .forms import petImageFormset
class DetailPetProfileView(LoginRequiredMixin, UpdateView):
    template_name = "profile/profile_pet.html"
    form_class = PetForm
    model = Pet
    
    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        petName = context['object'].name.title()
        context['titleTab'] = f'{petName} pet'
        context['object'] = Shelter.objects.get(manager= self.request.user)
        context['buttonName'] = f'Update {petName}'

        listImg = {}
        for i, img in enumerate(Images.objects.filter(pet=self.object)):
            listImg['id'+str(i)]= img.id
            listImg['img'+str(i)]= img.image
            listImg['mainPic'+str(i)]= img.mainPic

        data = {
                'form-TOTAL_FORMS':'2',
                'form-INITIAL_FORMS':'2',
                'form-MAX_NUM_FORMS': '2',
                
                # 'form-0-mainPic': '',
                # 'form-0-image': '',
                # 'form-0-id': '',
                # 'form-0-DELETE': 'on',
                
                'form-0-mainPic': listImg['mainPic0'],
                'form-0-image': listImg['img0'],
                'form-0-id': listImg['id0'],
                'form-0-DELETE': 'on',

                # 'form-1-mainPic': listImg['mainPic1'],
                # 'form-1-image': listImg['img1'],
                # 'form-1-id': listImg['id1'],
                # 'form-1-DELETE': 'on',
                
                # 'form-2-mainPic':listImg['mainPic2'],
                # 'form-2-image': listImg['img2'],
                # 'form-2-id': listImg['id2'],
                # 'form-2-DELETE': 'on',

            }
        context['formsetImg'] = petImageFormset(data, initial=[
                                # {'mainPic': d[0].image , 'image':d[0].mainPic},
                                # {'mainPic': d[1].image , 'image':d[1].mainPic},
                                ])
    
        return context

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

    def form_valid(self, form):
        
        formset = petImageFormset(self.request.POST, self.request.FILES)
        if formset.is_valid():
            for f in formset.cleaned_data:
                img = Images(pet=self.object, image=f['image'], mainPic=f['mainPic'])
                img.save()

        if form.is_valid():
            form.save()
        return super().form_valid(form)


class BaseProfileView (LoginRequiredMixin, TemplateView):
    template_name = "profile/profileSummarize.html"
    model = Shelter

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        shelter = Shelter.objects.get(manager= self.request.user)
        context['titleTab'] = f'Your {shelter.name}'
        context['object'] = shelter
        return context


class LazyReload(ListView):

    def get(self, request, *args, **kwargs):
        
        if self.request.is_ajax() and self.request.method == "GET":

            filters = {
                "status__in":["Urgent","Adoption"]
            }

            if self.kwargs.get("slug") is not None:
                # if we have a slug means we are in shelter, so we get rid of the first 4 
                # to avoid repetitions
                filters["shelter__slug"] = self.kwargs.get("slug")
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

# from .forms import petImageFormset
# class DetailPetProfileView(LoginRequiredMixin, UpdateView):
#     template_name = "profile/profile_pet.html"
#     form_class = PetForm
#     model = Pet

#     def get_context_data(self, **kwargs):
#         # Retrieves initial data
#         context = super().get_context_data(**kwargs)
#         # adds new data
#         petName = context['object'].name.title()
#         context['titleTab'] = f'{petName} pet'
#         context['object'] = Shelter.objects.get(manager= self.request.user)
#         context['buttonName'] = f'Update {petName}'
#         context['formsetPic'] = petImageFormset()
            
#         return context

#     def get_object(self, queryset=None):
#         #https://stackoverflow.com/questions/57614381/generic-detail-view-postdetailview-must-be-called-with-either-an-object-pk-or-a
#         # Since I'm using 2 variables in the url, django
#         # doesn't know how to use the second one.
#         if queryset is None:
#             queryset = self.get_queryset()
#         new_str = self.kwargs.get('pet') or self.request.GET.get('pet') or None

#         queryset = queryset.filter(slug=new_str)
#         obj = queryset.get()
#         return obj

#     def form_valid(self, form):
#         self.get_context_data()
#         petOrder = []
#         petImgs = Images.objects.filter(pet= self.object)
        
#         for pi in petImgs:
#             petOrder.append(pi)
#         pos = 0
#         for x, i in self.request.FILES.items():
#             try:
#                 Images.objects.filter(pk= petOrder[pos].pk).update(image=i)
#             except Exception as ex:
#                 img = Images(pet=self.object, image = i)
#                 img.save()
#         return super().form_valid(form)

        # data = {
        #         'form-TOTAL_FORMS':'2',
        #         'form-INITIAL_FORMS':'2',
        #         'form-MAX_NUM_FORMS': '2',
        #         'form-0-mainPic': d[0].mainPic,
        #         'form-0-image': d[0].image,
        #         'form-0-DELETE': 'on',
        #         'form-1-mainPic': d[1].mainPic,
        #         'form-1-image': d[1].image,
        #         'form-1-DELETE': 'on',
        #         'form-2-mainPic': d[2].mainPic,
        #         'form-2-image': d[2].image.url,
        #         'form-2-DELETE': 'on',

        #     }