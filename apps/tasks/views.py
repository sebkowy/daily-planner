from rest_framework import viewsets, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskTemplateSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['priority', 'task_type', 'is_cyclical']
    ordering_fields = ['priority', 'created_at', 'updated_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        elif user.department:
            return Task.objects.filter(created_by__department=user.department)
        else:
            return Task.objects.filter(created_by=user)


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['post'])
    def create_from_template(self, request):
        template = request.data.get('template')
        if not template:
            return Response({"error": "Template data is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskTemplateSerializer(data=template)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(created_by=request.user)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def templates(self, request):
        templates = Task.objects.filter(created_by=request.user, is_cyclical=True)
        serializer = TaskTemplateSerializer(templates, many=True)
        return Response(serializer.data)