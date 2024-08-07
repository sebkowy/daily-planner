from rest_framework import viewsets, permissions
from .models import Department
from .serializers import DepartmentSerializer, DepartmentDetailSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DepartmentDetailSerializer
        return DepartmentSerializer

    def perform_create(self, serializer):
        serializer.save()