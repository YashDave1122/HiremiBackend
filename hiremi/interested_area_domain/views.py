# from rest_framework import viewsets
# from .models import SelectedDomain
# from .serializers import SelectedDomainSerializer
# from django_filters.rest_framework import DjangoFilterBackend

# class SelectedDomainViewSet(viewsets.ModelViewSet):
#     serializer_class = SelectedDomainSerializer
#     queryset = SelectedDomain.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['register']

#     def get_queryset(self):
#         """
#         Optionally filters by register ID from query parameter
#         """
#         queryset = super().get_queryset()
#         register_id = self.request.query_params.get('register')
#         if register_id:
#             queryset = queryset.filter(register=register_id)
#         return queryset
    

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SelectedDomain
from .serializers import SelectedDomainSerializer

class SelectedDomainViewSet(viewsets.ModelViewSet):
    serializer_class = SelectedDomainSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter only current user's data"""
        return SelectedDomain.objects.filter(register=self.request.user)

    def create(self, request, *args, **kwargs):
        """Ensure a user can only have one entry"""
        if SelectedDomain.objects.filter(register=request.user).exists():
            return Response({"error": "You have already selected your domains. Use update instead."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Ensure users update their existing entry, not create new"""
        instance = SelectedDomain.objects.filter(register=request.user).first()
        if not instance:
            return Response({"error": "No record found. Please create one first."}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
