from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ApplicationViewSet, SkillViewSet, InterestViewSet, AskExpertViewSet,  UserProfileViewSet

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'interests', InterestViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'ask-expert', AskExpertViewSet, basename='askexpert')
urlpatterns = [
    path('', include(router.urls)),
]
