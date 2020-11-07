from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import ( HomeView, LazyReload, 
    DetailPetView, 
    ShelterView, DetailShelterView, CreateShelterView,
    BaseProfileView, UpdateShelterView,
    ListPetsView, ProfileOptionsShelter, DeleteShelterView,
    CreatePetProfileView, UpdatePetProfileView, DeletePetProfileView,
    CreateImageView, UpdateImageView, DeleteImageView
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
    path('profile/<slug:slug>/delete/', DeleteShelterView.as_view(), name="delete-profile"),
    path('profile/options/<slug:slug>/', ProfileOptionsShelter.as_view(), name="profile-options"),
    
    path('manager/pets/<slug:shelter>/', ListPetsView.as_view(), name="pets"),
    path('manager/pets/<slug:shelter>/create/', CreatePetProfileView.as_view(), name="pet-profile-create"),
    path('manager/pets/<slug:shelter>/<slug:pet>/', UpdatePetProfileView.as_view(), name="pet-profile-update"),
    path('manager/pets/<int:pk>/delete', DeletePetProfileView.as_view(), name="pet-profile-delete"),

    path('imagen/<slug:pet>/create/', CreateImageView.as_view(), name="pet-image-new"),
    path('imagen/<int:pk>/update/', UpdateImageView.as_view(), name="pet-image-update"),
    path('imagen/<int:pk>/delete/', DeleteImageView.as_view(), name="pet-image-delete")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
