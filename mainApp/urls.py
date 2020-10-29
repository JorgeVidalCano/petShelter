from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import HomeView, LazyReload, DetailPetView, ShelterView, DetailShelterView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('lazyReload/<int:page>', LazyReload.as_view(), name="lazy-reload"),
    path('lazyReload/<int:page>/<shelters>/<slug:slug>', LazyReload.as_view(), name="lazy-reload"),
    path('pet/<slug:slug>/', DetailPetView.as_view(), name="pet-detail"),
    path('shelters/', ShelterView.as_view(), name="shelter-list"),
    path('shelters/<slug:slug>/', DetailShelterView.as_view(), name="shelter-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
