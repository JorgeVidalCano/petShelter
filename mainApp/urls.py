from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import HomeView, LazyReload

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('lazyReload/', LazyReload.as_view(), name="lazy-reload")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
