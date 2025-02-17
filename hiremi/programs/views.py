from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Program, Enrollment
from .serializers import ProgramSerializer, EnrollmentSerializer

class ProgramViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Programs.
    - Only authenticated users can access.
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]  


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Enrollments.
    - Provides endpoints for all enrollments and user-specific enrollments.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        """
        If `user_id` is passed in the URL, return enrollments for that specific user.
        Otherwise, return all enrollments.
        """
        user_id = self.kwargs.get('user_id')
        if user_id:
            return Enrollment.objects.filter(user_id=user_id)
        return super().get_queryset()

    @action(detail=False, methods=['GET'])
    def user_enrollments(self, request, user_id=None):
        """
        Custom action to retrieve enrollments for a specific user.
        Endpoint: /accounts/{user_id}/enrollments/
        """
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        enrollments = Enrollment.objects.filter(user_id=user_id)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
