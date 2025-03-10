from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AccountViewSet, get_cities, get_state_cities, get_states

router = DefaultRouter()
router.register(r"accounts", AccountViewSet, basename="account")
# router.register(r"states", StateViewSet, basename="state")
# router.register(r"cities", CityViewSet, basename="city")

urlpatterns = [
    path("", include(router.urls)),
    path('states/', get_states, name='states'),
    path('cities/', get_cities, name='cities'),
    path('states/<str:state_name>/cities/', get_state_cities, name='state-cities'),

]
