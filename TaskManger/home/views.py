from django.http import HttpResponse,JsonResponse
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework import viewsets, status
from .models import TaskDetails
from .serializers import TaskDetailSerializer, UserSerializer
from rest_framework.response import Response


class TaskDetailViewSet(viewsets.ModelViewSet):
    queryset = TaskDetails.objects.all()
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        return TaskDetails.objects.filter(username=self.request.user.username)

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
