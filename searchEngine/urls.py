from django.urls import path, re_path
from searchEngine.views import SearchView, AjaxSearchView

urlpatterns = [
    path('', SearchView.as_view(), name='search-results'),    
    path('ajaxSearch/', AjaxSearchView.as_view(), name='ajaxSearch'),
]