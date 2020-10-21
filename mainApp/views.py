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
        
        filters = {
            "status__in":["Urgent","Adoption"]    
            }
        
        context['pets'] = Pet.objects.filter(**filters).order_by("?")

        shelters = Shelter.objects.order_by("?")[:2]
        copyNames=copy.copy(shelters) # shelters its a refval so it keeps changing
        
        # list of pets in shelters
        filters["shelter"] = shelters[0]
        context['petShelter1'] = Pet.objects.filter(**filters)[:6]
        
        filters["shelter"] = shelters[1]
        context['petShelter2'] = Pet.objects.filter(**filters)[:6]

        # shelters names
        context['shelterName1'] = copyNames[0]
        context['shelterName2'] = copyNames[1]

        return context

class LazyReload(ListView):

    # def get(self, request, *args, **kwargs):
        
    #     if self.request.is_ajax() and self.request.method == "GET":
    #         filters = {
    #             "status__in":["Urgent","Adoption"]    
    #         }
    #         # excludes = {
    #         #     "id":[load the list of animals]
    #         # }

    #         # if self.kwargs.get("tag") is not None:
    #             # tag = TagPost.objects.get(slug=slugify(self.kwargs.get('tag')))
    #             # filters["tags"] = tag

    #         try:
    #             self.pet_list = Pet.objects.filter(**filters).exclude(**excludes).order_by('-date_posted')
    #             self.page = self.selectPostsByPage(self.post_list)
    #             ser_instance = self.getPosts(self.page)
                
    #             return JsonResponse({"instance": ser_instance, "end": False}, status=200)
    #         except Exception as ex:
    #             print(ex)
    #             return JsonResponse({"instance": None, "end": True}, status=200)    
    
    def selectPostsByPage(self, post_list):
        # we select the next 5 posts
        numberPage = self.kwargs.get("page")
        splitPag = Paginator(self.post_list, 5)
        self.page = splitPag.page(numberPage)
        
        return self.page
    
    def getPosts(self, page_post):
        # we get the 5 posts and serialize them
        posts = self.preserializer(page_post)
        ser_instance = json.dumps(list(posts))    
        
        return ser_instance

    def preserializer(self, page_posts):
        # Because I was unable to retrieve the tags and author, I have to loop over through
        # the queryset and create a dict and add it to a list
        posts = []
        post = {}

        for p in page_posts.object_list:
            post = {
                "title": p.title.title(),
                "content": p.content,
                "image": p.PostImages.url,
                "datePosted": p.date_posted.strftime("%d-%b-%Y"),
                "author": p.author.username.title(),
                "slug": p.slug,
                "tags": [t.tag for t in p.findTags()]
            }
            
            posts.append(post)
        return posts

