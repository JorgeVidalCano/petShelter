from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import ( HomeView, LazyReload, 
    DetailPetView, 
    ShelterView, DetailShelterView, CreateShelterView,
    BaseProfileView, UpdateShelterView,
    ListShelterPetsView, ProfileOptionsShelter
)
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('lazyReload/<int:page>', LazyReload.as_view(), name="lazy-reload"),
    path('lazyReload/<int:page>/<shelters>/<slug:slug>', LazyReload.as_view(), name="lazy-reload"),
    path('pet/<slug:slug>/', DetailPetView.as_view(), name="pet-detail"),
    
    path('shelters/', ShelterView.as_view(), name="shelter-list"),
    path('shelters/new/', CreateShelterView.as_view(), name='shelter-new'),
    path('shelters/<slug:slug>/', DetailShelterView.as_view(), name="shelter-detail"),
    
    path('profile/', BaseProfileView.as_view(), name="profile"),
    path('profile/<slug:slug>/', UpdateShelterView.as_view(), name="profile-shelter"),
    path('profile/options/<slug:slug>/', ProfileOptionsShelter.as_view(), name="profile-options"),
    
    path('manager/pets/<slug:shelter>/', ListShelterPetsView.as_view(), name="pets"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
