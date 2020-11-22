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
    template_name = "mainApp/home.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titleTab'] = 'Home'

        context['title'] = f"Results for '{self.request.GET.get('q')}'"
        query = self.request.GET.get('q')
        post_list = Post.objects.filter( Q(title__icontains=query) & Q(publish=True) )
        context['posts'] = post_list
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

