from django.template.defaultfilters import slugify
from django.views.generic import ListView
from mainApp.models import Shelter, Pet
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.db.models import Q 
import datetime
import json


class SearchView(ListView):
    model = Pet
    template_name = "mainApp/searchResult.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        query = self.request.GET.get('q')
        shelter_list = Shelter.objects.filter( Q(name__icontains=query) | Q(location__icontains=query))[:6]
        
        context.update({
            'titleTab': 'Shelters',
            'title': f"Results for '{self.request.GET.get('q')}'",
            'shelter': shelter_list,
            'shelterId': [s.id for s in shelter_list] # we pass it so the lazy Search doesnot repeat
        })
        return context

class AjaxSearchView(ListView):
    ''' It handles the ajax response'''
    model = Shelter

    def get(self, request, *args, **kwargs):

        if self.request.is_ajax() and self.request.method == "GET":
            
            query = self.request.GET.get('q')
            objList = []
            obj = {}
            if query:
                querySet = Shelter.objects.filter( Q(name__icontains=query) | Q(location__icontains=query))[:6]

                for q in querySet:
                    obj = {
                        "name": q.name.title(),
                        "location": q.location,
                        "image": q.image.url,
                        "slug": q.slug,
                    }
                    objList.append(obj) 
            else:
                filters= {}
                query = self.request.GET.get('sex')
                if query != 'None':
                    filters["sex"] = query
                query = self.request.GET.get('kind')
                if query != 'None':
                    filters["kind"] = query
                query = self.request.GET.get('state')
                if query != 'None':
                    filters["status"] = query

                query = self.request.GET.get('pet')
                querySet = Pet.objects.filter(Q(name__icontains=query), **filters)[:8]

                for q in querySet:
                    obj = {
                        "title": q.name.title(),
                        "image": q.petMainPic(),
                        "slug": q.slug,
                    }
                    objList.append(obj) 

            instance = json.dumps(list(objList))

            return JsonResponse({"instance": instance}, status=200)
        return JsonResponse({"error": "No results"}, status=400)