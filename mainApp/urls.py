from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import HomeView, LazyReload, DetailPetView, ShelterView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('lazyReload/<int:page>', LazyReload.as_view(), name="lazy-reload"),
    path('lazyReload/<int:page>/<shelter>', LazyReload.as_view(), name="lazy-reload"),
    path('pet/<slug:slug>/', DetailPetView.as_view(), name="pet-detail"),
    path('shelters/', ShelterView.as_view(), name="shelter-list"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
