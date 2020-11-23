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
            if query is None:
                return JsonResponse({"error": "No results"}, status=400)
            
            querySet = Shelter.objects.filter( Q(name__icontains=query) | Q(location__icontains=query))[:6]

            objList = []
            obj = {}

            for q in querySet:
                obj = {
                    "title": q.name.title(),
                    "image": q.image.url,
                    "slug": q.slug,
                }
                objList.append(obj)
            instance = json.dumps(list(objList))
            return JsonResponse({"instance": instance}, status=200)

