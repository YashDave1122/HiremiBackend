
from rest_framework import viewsets, permissions
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
    - Only authenticated users can access.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]  
