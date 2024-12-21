from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth', include('authentications.rest.urls.authentications')),
    path('api/v1/categories', include('categories.urls')),
]
