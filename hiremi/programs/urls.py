# from django.urls import path
# from .views import ProgramListCreateView, ProgramDetailView, EnrollmentListCreateView, EnrollmentDetailView

# urlpatterns = [
    
#     # Program Endpoints
#     path('', ProgramListCreateView.as_view(), name='program-list'),
#     path('<int:pk>/', ProgramDetailView.as_view(), name='program-detail'),

#     # Enrollment Endpoints
#     path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list'),
#     path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
# ]




from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, EnrollmentViewSet

# Create a router and register our ViewSets
router = DefaultRouter()
router.register(r'programs', ProgramViewSet, basename='program')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

# Include the router URLs
urlpatterns = [
    path('', include(router.urls)),
]

