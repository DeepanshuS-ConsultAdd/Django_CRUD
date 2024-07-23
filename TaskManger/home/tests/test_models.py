import pytest
from home.models import TaskDetails
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_task_creation():
    user = User.objects.create_user(username='testuser', password='password')
    task = TaskDetails.objects.create(
        username=user.username,
        title='Test Task',
        description='A description',
        due_date='2024-12-31',
        priority=1,
        category='General'
    )
    
    # Assertions
    assert task.username == 'testuser'
    assert task.title == 'Test Task'
    assert task.description == 'A description'
    assert task.due_date == '2024-12-31'
    assert task.priority == 1
    assert task.category == 'General'
