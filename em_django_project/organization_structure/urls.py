from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DepartmentViewSet, EmployeeViewSet, PositionViewSet

router = DefaultRouter()
router.register(r"department", DepartmentViewSet)
router.register(r"position", PositionViewSet)
router.register(r"employee", EmployeeViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
