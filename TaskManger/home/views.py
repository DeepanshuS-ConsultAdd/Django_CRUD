from django.http import HttpResponse,JsonResponse
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework import viewsets, status
from .models import TaskDetails
from .serializers import TaskDetailSerializer, UserSerializer
from rest_framework.response import Response
from datetime import datetime, date

class TaskDetailViewSet(viewsets.ModelViewSet):
    queryset = TaskDetails.objects.all()
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        return TaskDetails.objects.filter(username=self.request.user.username).order_by('priority','-due_date')

    def perform_create(self, serializer):
        if self.request.user.username != self.request.data.get('username'):
            raise ValidationError("Username in the request data does not match the authenticated user.")
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.username != serializer.instance.username:
            raise ValidationError("You can only update your own tasks.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.username != instance.username:
            raise ValidationError("You can only delete your own tasks.")
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        existing_serializer = self.get_serializer(instance)

        existing_data = existing_serializer.data        
        new_data = serializer.validated_data
        
        new_data_normalized = {
            key: str(value) if isinstance(value, (datetime, date)) else value
            for key, value in new_data.items()
        }

        if not any(str(existing_data.get(field)) != str(new_data_normalized.get(field)) for field in new_data):
            return Response({"detail": "No fields have been changed."}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response({"detail": "Task updated successfully."}, status=status.HTTP_200_OK)

    
def home(request):
    return HttpResponse("<h1>Heyh! Home Page<h1>")


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AllTaskListView(generics.ListAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [permissions.IsAdminUser]  

    def get_queryset(self):
        return TaskDetails.objects.all()
    
