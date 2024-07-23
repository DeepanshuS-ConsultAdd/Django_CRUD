from rest_framework import serializers
from .models import TaskDetails
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskDetails
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        return user
