from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExperienceViewSet, ProjectViewSet, SocialLinkViewSet, EducationViewSet

router = DefaultRouter()
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'social_links', SocialLinkViewSet, basename='social_link')
router.register(r'education', EducationViewSet, basename='education')

urlpatterns = [
    path("", include(router.urls)),  # Standard list/detail routes
]
