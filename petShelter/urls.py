from django.contrib.auth import views as auth_views
from users.views import MyLoginView, DeleteAccount, RegisterAccount
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterAccount.as_view(), name='register'),
    path('login/', MyLoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('deleteAccount/<int:pk>', DeleteAccount.as_view(), name='delete-account'),
    path('message/', include('contactMessages.urls')),
    path('search/', include('searchEngine.urls')),
    path('', include('mainApp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
