from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'programs', ProgramViewSet, basename='program')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),

    # Custom User-Specific Enrollment Endpoints
    path('accounts/<int:user_id>/enrollments/', EnrollmentViewSet.as_view({'get': 'user_enrollments', 'post': 'create'}), name='user-enrollments'),
    path('accounts/<int:user_id>/enrollments/<int:pk>/', EnrollmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-enrollment-detail'),
]
