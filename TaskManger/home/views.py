# from django.http import HttpResponse,JsonResponse
# from rest_framework.exceptions import ValidationError
# from django.contrib.auth.models import User
# from rest_framework import generics, permissions
# from rest_framework import viewsets, status
# from .models import TaskDetails
# from .serializers import TaskDetailSerializer, UserSerializer
# from rest_framework.response import Response
# from datetime import datetime, date
# from rest_framework.views import APIView


# class TaskDetailViewSet(viewsets.ModelViewSet):
#     queryset = TaskDetails.objects.all()
#     serializer_class = TaskDetailSerializer

#     def get_queryset(self):
#         return TaskDetails.objects.filter(username=self.request.user.username).order_by('priority','-due_date')

#     def perform_create(self, serializer):
#         if self.request.user.username != self.request.data.get('username'):
#             raise ValidationError("Username in the request data does not match the authenticated user.")
#         serializer.save()

#     def perform_update(self, serializer):
#         if self.request.user.username != serializer.instance.username:
#             raise ValidationError("You can only update your own tasks.")
#         serializer.save()

#     def perform_destroy(self, instance):
#         if self.request.user.username != instance.username:
#             raise ValidationError("You can only delete your own tasks.")
#         instance.delete()
    
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response({"detail": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)

#         serializer.is_valid(raise_exception=True)
#         existing_serializer = self.get_serializer(instance)

#         existing_data = existing_serializer.data        
#         new_data = serializer.validated_data
        
#         new_data_normalized = {
#             key: str(value) if isinstance(value, (datetime, date)) else value
#             for key, value in new_data.items()
#         }

#         if not any(str(existing_data.get(field)) != str(new_data_normalized.get(field)) for field in new_data):
#             return Response({"detail": "No fields have been changed."}, status=status.HTTP_400_BAD_REQUEST)
        
#         self.perform_update(serializer)
#         return Response({"detail": "Task updated successfully."}, status=status.HTTP_200_OK)

    
# def home(request):
#     return HttpResponse("<h1>Heyh! Home Page<h1>")


# class UserCreateView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]

# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class AllTaskListView(generics.ListAPIView):
#     serializer_class = TaskDetailSerializer
#     permission_classes = [permissions.IsAdminUser]  

#     def get_queryset(self):
#         return TaskDetails.objects.all()
    
# class TaskByDateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, date_str, *args, **kwargs):
#         try:
#             search_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#         except ValueError:
#             return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

#         tasks = TaskDetails.objects.filter(username=request.user.username, due_date=search_date)
#         serializer = TaskDetailSerializer(tasks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

import logging
from django.http import HttpResponse, JsonResponse
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework import viewsets, status
from .models import TaskDetails
from .serializers import TaskDetailSerializer, UserSerializer
from rest_framework.response import Response
from datetime import datetime, date
from rest_framework.views import APIView

logger = logging.getLogger('home')

class TaskDetailViewSet(viewsets.ModelViewSet):
    queryset = TaskDetails.objects.all()
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        logger.debug(f'User {self.request.user.username} is retrieving tasks.')
        return TaskDetails.objects.filter(username=self.request.user.username).order_by('priority', '-due_date')

    def perform_create(self, serializer):
        if self.request.user.username != self.request.data.get('username'):
            logger.warning(f'User {self.request.user.username} attempted to create a task for {self.request.data.get("username")}.')
            raise ValidationError("Username in the request data does not match the authenticated user.")
        serializer.save()
        logger.info(f'Task created for user {self.request.user.username}.')

    def perform_update(self, serializer):
        if self.request.user.username != serializer.instance.username:
            logger.warning(f'User {self.request.user.username} attempted to update a task for {serializer.instance.username}.')
            raise ValidationError("You can only update your own tasks.")
        serializer.save()
        logger.info(f'Task updated for user {self.request.user.username}.')

    def perform_destroy(self, instance):
        if self.request.user.username != instance.username:
            logger.warning(f'User {self.request.user.username} attempted to delete a task for {instance.username}.')
            raise ValidationError("You can only delete your own tasks.")
        instance.delete()
        logger.info(f'Task deleted for user {self.request.user.username}.')

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
            logger.info(f'No fields changed for task {instance.id} by user {request.user.username}.')
            return Response({"detail": "No fields have been changed."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        logger.info(f'Task {instance.id} updated by user {request.user.username}.')
        return Response({"detail": "Task updated successfully."}, status=status.HTTP_200_OK)


def home(request):
    logger.info('Home page accessed.')
    return HttpResponse("<h1>Heyh! Home Page<h1>")


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        logger.info(f'New user created: {serializer.validated_data["username"]}')
        serializer.save()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.debug('User list accessed.')
        return super().get_queryset()


class AllTaskListView(generics.ListAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [permissions.IsAdminUser]  

    def get_queryset(self):
        logger.debug('All tasks list accessed by admin.')
        return TaskDetails.objects.all()


class TaskByDateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, date_str, *args, **kwargs):
        try:
            search_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            logger.error(f'Invalid date format: {date_str}')
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        tasks = TaskDetails.objects.filter(username=request.user.username, due_date=search_date)
        serializer = TaskDetailSerializer(tasks, many=True)
        logger.debug(f'Tasks retrieved for date {search_date} by user {request.user.username}.')
        return Response(serializer.data, status=status.HTTP_200_OK)

