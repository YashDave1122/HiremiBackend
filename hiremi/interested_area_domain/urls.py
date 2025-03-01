# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import SelectedDomainViewSet

# router = DefaultRouter()
# router.register(r'selectedDomain', SelectedDomainViewSet)

# urlpatterns = [
#     path('api/', include(router.urls)),
# ]






from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SelectedDomainViewSet

router = DefaultRouter()
router.register(r'selected-domains', SelectedDomainViewSet, basename='selected-domain')

urlpatterns = [
    path('api/', include(router.urls)),
]

