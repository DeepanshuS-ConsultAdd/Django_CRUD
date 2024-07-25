import pytest
import base64
from rest_framework import status
from django.contrib.auth.models import User
from home.models import TaskDetails
from rest_framework.test import APIClient

def encode_credentials(username, password):
    credentials = f'{username}:{password}'
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f'Basic {encoded_credentials}'


@pytest.mark.django_db
def test_user_task_list():
    myusername='testuser'
    mypassword='password'
    user = User.objects.create_user(username=myusername, password=mypassword)
    TaskDetails.objects.create(username=myusername, title='Test Task')
    
    client = APIClient()
    client.login(username=myusername, password=mypassword)
    auth_header = encode_credentials(myusername, mypassword)
    client.credentials(HTTP_AUTHORIZATION=auth_header)  
    response = client.get('/api/taskdetails/')
    
    print("Response data:", response.data)
    print("Response status code:", response.status_code)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'Test Task'

@pytest.mark.django_db
def test_user_registration(client):
    myusername='newuser'
    mypassword='newpassword'
    response = client.post('/api/register/', {
        'username': myusername,
        'password': mypassword
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username=myusername).exists()

@pytest.mark.django_db
def test_user_login(client):

    myusername='testuser'
    mypassword='password'
    user = User.objects.create_user(username=myusername, password=mypassword)
    client = APIClient()
    client.login(username=myusername, password=mypassword)
    auth_header = encode_credentials(myusername, mypassword)
    client.credentials(HTTP_AUTHORIZATION=auth_header)      
    response = client.get('/api/users/')
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_unaouth_user_login(client):

    myusername='testuser'
    mypassword='password'
    user = User.objects.create_user(username=myusername, password=mypassword)
    response = client.get('/api/users/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_task_creation_same_user(client):
    myusername='testuser'
    mypassword='password'
    user = User.objects.create_user(username=myusername, password=mypassword)
    TaskDetails.objects.create(username=myusername, title='Test Task')
    
    client = APIClient()
    client.login(username=myusername, password=mypassword)
    auth_header = encode_credentials(myusername, mypassword)
    client.credentials(HTTP_AUTHORIZATION=auth_header)

    response = client.post('/api/taskdetails/', {
        'username': myusername,
        'title': 'Test Task',
        'description': 'Changed test..',
        'due_date': "2024-09-09"
    })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'Test Task'
    assert response.data['username'] == myusername

@pytest.mark.django_db
def test_task_creation_different_user(client):

    myusername='testuser'
    mypassword='password'
    user = User.objects.create_user(username=myusername, password=mypassword)
    client = APIClient()
    client.login(username=myusername, password=mypassword)
    auth_header = encode_credentials(myusername, mypassword)
    client.credentials(HTTP_AUTHORIZATION=auth_header)  

    response = client.post('/api/taskdetails/', {
        'username': 'testuser1',
        'title': 'Test Task',
        'description': 'Changed test..',
        'due_date': "2024-09-09"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_task_updation_same_user(client):

    myusername='testuser'
    mypassword='password'
    User.objects.create_user(username=myusername, password=mypassword)
    client = APIClient()
    client.login(username=myusername, password=mypassword)
    auth_header = encode_credentials(myusername, mypassword)
    client.credentials(HTTP_AUTHORIZATION=auth_header)  

    response = client.post('/api/taskdetails/', {
        'username': myusername,
        'title': 'Test Task',
        'due_date': "2024-09-09",
        'description': 'Changed test..'
    })
    
    response2 = client.get('/api/taskdetails/')
    response1 =client.put(f'/api/taskdetails/{response2.data[0]['id']}/', {
        'username': myusername,
        'title': 'PUT CHECK',
        'due_date': "2024-08-08",
        'description': 'Changed testtt..',
    }) 
    
    print("Response data:", response.data)
    print("Response status code:", response.status_code)
    print("Response data:", response1.data)
    print("Response status code:", response1.status_code)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == myusername
    assert response.data['title'] == 'Test Task'

    assert response1.status_code == status.HTTP_200_OK    

@pytest.mark.django_db
def test_task_updation_diff_user(client):

    myusername='testuser1'
    mypassword='password1'
    User.objects.create_user(username=myusername, password=mypassword)
    client = APIClient()
    client.login(username=myusername, password=mypassword)
    auth_header = encode_credentials(myusername, mypassword)
    client.credentials(HTTP_AUTHORIZATION=auth_header)   

    response = client.post('/api/taskdetails/', {
        'username': 'testuser1',
        'title': 'Test Task',
        'due_date': "2024-09-09",
        'description': 'Changed test..'
    }) 

    myusername1='testuser'
    mypassword1='password'
    User.objects.create_user(username=myusername1, password=mypassword1)
    client1 = APIClient()
    client1.login(username=myusername1, password=mypassword1)
    auth_header = encode_credentials(myusername1, mypassword1)
    client1.credentials(HTTP_AUTHORIZATION=auth_header) 

    response2 = client.get('/api/taskdetails/')
    response1 =client1.put(f'/api/taskdetails/{response2.data[0]['id']}/', {
        'username': 'testuser',
        'title': 'PUT CHECK Change',
        'due_date': "2024-09-09"
    }) 
    
    print("Response data:", response.data)
    print("Response status code:", response.status_code)
    print("Response data:", response1.data)
    print("Response status code:", response1.status_code)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == myusername
    assert response.data['title'] == 'Test Task'

    assert response1.status_code == status.HTTP_404_NOT_FOUND
    

@pytest.mark.django_db
def test_task_delete_same_user(client):

    myusername='testuser1'
    mypassword='password1'
    User.objects.create_user(username=myusername, password=mypassword)
    client = APIClient()
    client.login(username=myusername, password=mypassword)
    auth_header = encode_credentials(myusername, mypassword)
    client.credentials(HTTP_AUTHORIZATION=auth_header)   

    client.post('/api/taskdetails/', {
        'username': myusername,
        'title': 'Test Task',
        'due_date': "2024-09-09",
        'description': 'Changed test..'
    })  

    response2 = client.get('/api/taskdetails/')
    response = client.delete(f'/api/taskdetails/{response2.data[0]['id']}/')

    print(response2.data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_task_delete_diff_user(client):

    myusername='testuser1'
    mypassword='password1'
    User.objects.create_user(username=myusername, password=mypassword)
    client = APIClient()
    client.login(username=myusername, password=mypassword)
    auth_header = encode_credentials(myusername, mypassword)
    client.credentials(HTTP_AUTHORIZATION=auth_header) 

    client.post('/api/taskdetails/', {
        'username': myusername,
        'title': 'Test Task',
        'description': 'Changed test..',
        'due_date': "2024-09-09"
    })

    myusername1='testuser'
    mypassword1='password'
    User.objects.create_user(username=myusername1, password=mypassword1)
    client1 = APIClient()
    client1.login(username=myusername1, password=mypassword1)
    auth_header = encode_credentials(myusername1, mypassword1)
    client1.credentials(HTTP_AUTHORIZATION=auth_header)  

    response2 = client.get('/api/taskdetails/')
    response = client1.delete(f'/api/taskdetails/{response2.data[0]['id']}/')

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_superuser_access(client):
    myusername='admin'
    mypassword='adminpass'
    User.objects.create_superuser(username=myusername, password=mypassword)
    client = APIClient()
    client.login(username=myusername, password=mypassword)
    auth_header = encode_credentials(myusername, mypassword)
    client.credentials(HTTP_AUTHORIZATION=auth_header)  
    response = client.get('/api/alltasks/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_undefined(client):
    myusername1='testuser'
    mypassword1='password'
    User.objects.create_user(username=myusername1, password=mypassword1)
    client1 = APIClient()
    client1.login(username=myusername1, password=mypassword1)
    auth_header = encode_credentials(myusername1, mypassword1)
    client1.credentials(HTTP_AUTHORIZATION=auth_header) 

    response = client1.get('/api/taskdetails/1000/')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_delete_undefined(client):
    myusername1='testuser'
    mypassword1='password'
    User.objects.create_user(username=myusername1, password=mypassword1)
    client1 = APIClient()
    client1.login(username=myusername1, password=mypassword1)
    auth_header = encode_credentials(myusername1, mypassword1)
    client1.credentials(HTTP_AUTHORIZATION=auth_header) 

    response = client1.delete('/api/taskdetails/1000/')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_put_no_change_data(client):

    myusername='testuser'
    mypassword='password'
    User.objects.create_user(username=myusername, password=mypassword)
    client = APIClient()
    client.login(username=myusername, password=mypassword)
    auth_header = encode_credentials(myusername, mypassword)
    client.credentials(HTTP_AUTHORIZATION=auth_header)  

    response = client.post('/api/taskdetails/', {
        'username': myusername,
        'title': 'Test Task',
        'due_date': "2024-09-09",
        'description': 'Changed test..'
    })
    
    response2 = client.get('/api/taskdetails/')
    response1 =client.put(f'/api/taskdetails/{response2.data[0]['id']}/', {
        'username': myusername,
        'title': 'Test Task',
        'due_date': "2024-09-09",
        'description': 'Changed test..'
    }) 
    
    print("Response data:", response.data)
    print("Response status code:", response.status_code)
    print("Response data:", response1.data)
    print("Response status code:", response1.status_code)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == myusername
    assert response.data['title'] == 'Test Task'

    assert response1.status_code == status.HTTP_400_BAD_REQUEST 