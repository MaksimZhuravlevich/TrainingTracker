from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # без namespace
    path('core/', include('core.urls')),  # без namespace
    path('nutrition/', include('nutrition.urls')),  # без namespace
    path('users/', include(('users.urls', 'users'), namespace='users')),  # ТОЛЬКО users с namespace!
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)