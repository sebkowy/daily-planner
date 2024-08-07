from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'task_type', 'duration', 'is_cyclical', 'cycle_time', 'created_by', 'created_at', 'updated_at', 'priority', 'priority_display']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'task_type', 'duration', 'is_cyclical', 'cycle_time']
        read_only_fields = ['id']