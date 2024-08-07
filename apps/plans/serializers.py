from rest_framework import serializers
from .models import DailyPlan, DailyPlanTask, MonthlyPlan
from apps.tasks.serializers import TaskSerializer
from apps.users.serializers import UserSerializer

class DailyPlanTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    task_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = DailyPlanTask
        fields = ['id', 'daily_plan', 'task', 'task_id', 'start_time', 'end_time']
        read_only_fields = ['id']

    def create(self, validated_data):
        task_id = validated_data.pop('task_id')
        task = Task.objects.get(id=task_id)
        return DailyPlanTask.objects.create(task=task, **validated_data)

class DailyPlanSerializer(serializers.ModelSerializer):
    plan_tasks = DailyPlanTaskSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = DailyPlan
        fields = ['id', 'date', 'user', 'plan_tasks']

class MonthlyPlanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MonthlyPlan
        fields = ['id', 'month', 'year', 'user']