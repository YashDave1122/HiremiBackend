from rest_framework import viewsets, permissions
from .models import Query
from .serializers import QuerySerializer

class QueryViewSet(viewsets.ModelViewSet):
    
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)
