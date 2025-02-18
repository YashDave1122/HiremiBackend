from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AccountViewSet, CityViewSet, StateViewSet

router = DefaultRouter()
router.register(r"accounts", AccountViewSet, basename="account")
router.register(r"states", StateViewSet, basename="state")
router.register(r"cities", CityViewSet, basename="city")

urlpatterns = [
    path("", include(router.urls)),
]
