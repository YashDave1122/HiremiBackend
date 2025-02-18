from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Experience, Project, SocialLink, Education
from .serializers import ExperienceSerializer, ProjectSerializer, SocialLinkSerializer, EducationSerializer
from accounts.permissions import IsOwner

class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        if user_id:
            return Experience.objects.filter(user_id=user_id)
        return Experience.objects.all()

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_id")
        if user_id:
            serializer.save(user_id=user_id)
        else:
            serializer.save()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsOwner()]


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        if user_id:
            return Project.objects.filter(user_id=user_id)
        return Project.objects.all()

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_id")
        if user_id:
            serializer.save(user_id=user_id)
        else:
            serializer.save()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsOwner()]
    

class SocialLinkViewSet(viewsets.ModelViewSet):
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        if user_id:
            return SocialLink.objects.filter(user_id=user_id)
        return SocialLink.objects.all()

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_id")
        if user_id:
            serializer.save(user_id=user_id)
        else:
            serializer.save()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsOwner()]
    

class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        if user_id:
            return Education.objects.filter(user_id=user_id)
        return Education.objects.all()

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_id")
        if user_id:
            serializer.save(user_id=user_id)
        else:
            serializer.save()

    def get_permission_classes(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsOwner()]
