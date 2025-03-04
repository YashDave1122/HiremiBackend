from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Job, Application, Skill, Interest, UserProfile, AskExpert
from .serializers import JobSerializer, ApplicationSerializer, SkillSerializer, InterestSerializer,AskExpertSerializer, UserProfileSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

class AskExpertViewSet(viewsets.ModelViewSet):
    queryset = AskExpert.objects.all()
    serializer_class = AskExpertSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
  

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
