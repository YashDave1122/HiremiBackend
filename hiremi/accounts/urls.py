from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AccountViewSet, CityViewSet, EducationViewSet, StateViewSet

router = DefaultRouter()
router.register(r"(?P<user_id>\d)/education", EducationViewSet, basename="education")
router.register(r"accounts", AccountViewSet, basename="account")
router.register(r"states", StateViewSet, basename="state")
router.register(r"cities", CityViewSet, basename="city")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:user_id>/education/",
        EducationViewSet.as_view({"get": "list", "post": "create"}),
        name="education-list",
    ),
    path(
        "<int:user_id>/education/<int:pk>/",
        EducationViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="education-detail",
    ),
]
