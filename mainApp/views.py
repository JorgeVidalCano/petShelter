from django.shortcuts import render
from django.views.generic import(
     ListView, 
     DetailView, 
     CreateView,
     UpdateView,
     DeleteView,
     RedirectView,
     TemplateView
    )
from .models import Pet, Shelter
import copy
import json
from django.core.paginator import Paginator
from django.http import JsonResponse

class HomeView(TemplateView):
    template_name = "mainApp/home.html"
    model = Pet
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Home'
        
        filters = {"status__in":["Urgent","Adoption"]}
        
        context['pets'] = Pet.objects.filter(**filters).order_by("?") # all pets
        shelters = Shelter.objects.order_by("?")[:2]
        
        # list of pets in shelters
        filters["shelter"] = shelters[0]
        context['petShelter1'] = Pet.objects.filter(**filters)[:6]
        
        filters["shelter"] = shelters[1]
        context['petShelter2'] = Pet.objects.filter(**filters)[:6]

        # shelters names
        copyNames=copy.copy(shelters) # shelters are a refval so it keeps changing
        context['shelterName1'] = copyNames[0]
        context['shelterName2'] = copyNames[1]

        return context

class LazyReload(ListView):

    def get(self, request, *args, **kwargs):
        
         if self.request.is_ajax() and self.request.method == "GET":

            
            filters = {
                "status__in":["Urgent","Adoption"]    
            }
            excludes = {}
            # excludes = {
            #     "id":[load the list of animals]
            # }

            # if self.kwargs.get("tag") is not None:
                # tag = TagPost.objects.get(slug=slugify(self.kwargs.get('tag')))
                # filters["tags"] = tag

            try:
                self.pet_list = Pet.objects.filter(**filters).exclude(**excludes).order_by('-date_created')
                self.page = self.selectPetsByPage(self.pet_list)
                print(self.page)
                ser_instance = self.getPets(self.page)
                # print("HERE")
                # print(self.ser_instance)
                return JsonResponse({"instance": ser_instance, "end": False}, status=200)
            except Exception as ex:
                print(ex)
                return JsonResponse({"instance": None, "end": True}, status=200)    
    
    def selectPetsByPage(self, pet_list):
        # we select the next 6 pets
        numberPage = self.kwargs.get("page")
        splitPag = Paginator(self.pet_list, 2)
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
                "name": p.name,
                "sex": p.sex,
                "status": p.status,
                "shelter": p.shelter.name, 
                #"images": p.images.Images.url,
                "slug" : p.slug
            }
            print(p.images.url)
            # print(p.images.Images.url)
            pets.append(pet)
        return pets

