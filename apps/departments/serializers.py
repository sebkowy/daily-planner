from rest_framework import serializers
from .models import Department
from apps.users.serializers import UserSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']

class DepartmentDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'members']