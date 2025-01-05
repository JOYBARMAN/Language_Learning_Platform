from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("shared.swagger")),
    path("admin/", admin.site.urls),
    path("api/v1/auth", include("authentications.rest.urls.authentications")),
    path("api/v1/me", include("core.urls")),
    path("api/v1/categories", include("categories.urls")),
    path("api/v1/courses", include("courses.urls")),
]
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]