from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'programs', ProgramViewSet, basename='program')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')


urlpatterns = [
    path('', include(router.urls)),
]
