from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("registration.urls")),
    path("tasks/", include("tasks.urls")),
    path("organizations/", include("organization_structure.urls")),
]
