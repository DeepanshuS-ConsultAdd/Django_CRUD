from datetime import datetime
from rest_framework import serializers
from .models import TaskDetails
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import date


class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskDetails
        fields = "__all__"

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value

    def validate_due_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate_priority(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Priority must be between 1 and 5.")
        return value
    
    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError("Category is required.")
        if not isinstance(value, str):
            raise serializers.ValidationError("Category must be a string.")
        return value

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
