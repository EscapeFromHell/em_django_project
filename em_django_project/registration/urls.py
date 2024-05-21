from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationViewSet

router = DefaultRouter()
router.register(r"", RegistrationViewSet, basename="registration")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
