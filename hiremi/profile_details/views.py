from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Experience, Project, SocialLink, Education, Language
from .serializers import (ExperienceSerializer, ProjectSerializer, 
                        SocialLinkSerializer, EducationSerializer, LanguageSerializer)
from accounts.permissions import IsOwner, IsOwnerOrReadOnly

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filterset_fields = ["user", "company_name", "job_title"]
    search_fields = ["company_name", "job_title"]
    ordering_fields = []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filterset_fields = ["user"]
    search_fields = ["name"]
    ordering_fields = []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class SocialLinkViewSet(viewsets.ModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filterset_fields = ["user", "platform"]
    ordering_fields = []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filterset_fields = ["user", "degree", "branch", "passing_year","college_name","college_state","college_city"]
    search_fields = ["college_name", "branch", "degree"]
    ordering_fields = ["passing_year"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class LanguageViewSet(viewsets.ModelViewSet):
    serializer_class = LanguageSerializer
    # permission_classes = [IsStaff]
    queryset = Language.objects.all()