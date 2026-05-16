from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('core/', include('core.urls')),
    path('nutrition/', include('nutrition.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('generators/', include(('generators.urls', 'generators'), namespace='generators')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
