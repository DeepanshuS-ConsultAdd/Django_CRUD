from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from home.views import TaskDetailViewSet,home,UserCreateView,UserListView,AllTaskListView

router = DefaultRouter()
router.register(r'taskdetails', TaskDetailViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('api/', include(router.urls)),
    path('api/register/', UserCreateView.as_view(), name='user-register'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/alltasks/', AllTaskListView.as_view(), name='all-tasks'),
]
