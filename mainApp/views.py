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
from .forms import ShelterForm

ROWPET = 3 # amount of pets per row

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

class CreateShelterView(CreateView):
    #permision_required = ""
    template_name = "forms/shelter.html"
    form_class = ShelterForm
    model = Shelter
    
    def get_context_data(self, **kwargs):
        # Retrieves initial data
        context = super().get_context_data(**kwargs)
        # adds new data
        context['titleTab'] = 'Create New shelter'
        
        return context

    def form_valid(self, form):
        # Adds the author to the post
        #form.instance.author = self.request.user
        super().form_valid(form)
        
    
        # only access if some pic is uploaded
        if bool(self.request.FILES):
            form.instance.image = self.request.FILES['image']
        form.instance.slug = self.slugifier(self.request.POST['name'])
        return super().form_valid(form)


    
    

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

