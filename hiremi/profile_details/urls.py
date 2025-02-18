from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExperienceViewSet, ProjectViewSet, SocialLinkViewSet, EducationViewSet

router = DefaultRouter()
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'social-links', SocialLinkViewSet, basename='social-link')
router.register(r'education', EducationViewSet, basename='education')

urlpatterns = [
    path("", include(router.urls)),  # Standard list/detail routes

    # User-specific endpoints
    path(
        "accounts/<int:user_id>/experiences/",
        ExperienceViewSet.as_view({"get": "list", "post": "create"}),
        name="user-experience-list",
    ),
    path(
        "accounts/<int:user_id>/experiences/<int:pk>/",
        ExperienceViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy",}),
        name="user-experience-detail",
    ),

    path(
        "accounts/<int:user_id>/projects/",
        ProjectViewSet.as_view({"get": "list", "post": "create"}),
        name="user-project-list",
    ),
    path(
        "accounts/<int:user_id>/projects/<int:pk>/",
        ProjectViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy",}),
        name="user-project-detail",
    ),

    path(
        "accounts/<int:user_id>/social-links/",
        SocialLinkViewSet.as_view({"get": "list", "post": "create"}),
        name="user-social-link-list",
    ),
    path(
        "accounts/<int:user_id>/social-links/<int:pk>/",
        SocialLinkViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy",}),
        name="user-social-link-detail",
    ),

    path(
        "accounts/<int:user_id>/education/",
        EducationViewSet.as_view({"get": "list", "post": "create"}),
        name="user-education-list",
    ),
    path(
        "accounts/<int:user_id>/education/<int:pk>/",
        EducationViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy",}),
        name="user-education-detail",
    ),
]
