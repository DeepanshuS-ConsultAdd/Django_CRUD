## TASK MANAGER
In the Task Manager application, the first user must register. Since the username is unique, it ensures that users are authorized to access their own tasks. For operations such as creating, updating, and deleting tasks, the username provided in the Basic Authentication must match the username associated with the request. This prevents users from accessing each other's resources.

With Basic Authentication in place, if a user tries to access records belonging to another user, the request will be denied. Both the username used in Basic Authentication and the username associated with the task must match for the operation to succeed.

markdown
Copy code
# Django Project Setup Instructions

## Prerequisites

Ensure you have Python 3 installed. You can check this by running:

```bash
python3 --version
1. Create a Virtual Environment
Open your terminal and navigate to your project directory or create a new directory:
```

```bash
Copy code
mkdir my_project
cd my_project
Create a virtual environment:
```

```bash
Copy code
python3 -m venv venv
Activate the virtual environment:
```

```bash
Copy code
source venv/bin/activate
2. Install Dependencies
Install the required dependencies using pip:
```

```bash
pip install django djangorestframework psycopg2-binary
```
If you have a requirements.txt file with dependencies listed, you can install them using:


```bash
pip install -r requirements.txt
```

3. Create a Django Project and App
Create a new Django project:

```bash
Copy code
django-admin startproject myproject
cd myproject
```
```bash
python manage.py startapp home
```
4. Configure Database Settings
Edit the settings.py file in the myproject/myproject/settings.py directory to configure the database settings:

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Replace 'your_database_name', 'your_database_user', and 'your_database_password' with your PostgreSQL database credentials.
```

5. Apply Migrations
Apply the initial migrations to set up the database schema:

```bash
python manage.py migrate
```

6. Run the Development Server
Start the Django development server to check if everything is set up correctly:

```bash
python manage.py runserver
Visit http://127.0.0.1:8000/ in your web browser to see the Django welcome page.
```

#### USER CREATION 
<img width="1069" alt="image" src="https://github.com/user-attachments/assets/4693c8f5-c8bc-4e52-8d38-8335d1fbcbc4">

#### USER'S LIST
<img width="1058" alt="image" src="https://github.com/user-attachments/assets/8f71ac34-2af5-4882-9768-3e85b1e956ad">

#### USER TASKS
<img width="1061" alt="image" src="https://github.com/user-attachments/assets/9269d7d6-d3cf-47ab-9b1f-2cfdc19ab471">

#### ADDING USER TASK -(a)
<img width="1064" alt="image" src="https://github.com/user-attachments/assets/0304c2fd-1bb4-459b-9639-13bd899d25d0">

#### ADDING USER TASK -(b)
<img width="1060" alt="image" src="https://github.com/user-attachments/assets/78d0b2c4-3282-406a-a4b6-0f4ae80072e9">

#### PUT USER TASK
<img width="1064" alt="image" src="https://github.com/user-attachments/assets/855fd57e-4078-47ae-bcdb-45fafbb2a61b">

#### DELETE USER TASK
<img width="1017" alt="image" src="https://github.com/user-attachments/assets/43d539c3-5be3-4e54-a48d-8e57a9c26752">

#### OUTPUT
<img width="1054" alt="image" src="https://github.com/user-attachments/assets/47d94aa2-a927-4321-ab32-4e9e81883471">

#### Super User (Access to view All data)
<img width="1057" alt="image" src="https://github.com/user-attachments/assets/0b90046f-73da-40c2-9889-a739c93bea2a">

## Record for (myuser)
<img width="1073" alt="image" src="https://github.com/user-attachments/assets/3abec1f9-2842-4e80-8b0d-394d080d24b1">

#### Making POST Request using different account for a different user -(a)

<img width="1015" alt="image" src="https://github.com/user-attachments/assets/92003fa5-45b4-4e55-9989-7c4ebf21353c">

#### Making POST Request using different account for a different user -(b)

<img width="1057" alt="image" src="https://github.com/user-attachments/assets/0e33ecae-e340-4b39-9288-0f050929ecff">

#### Making PUT Request using different account for a different user -(a)
<img width="1054" alt="image" src="https://github.com/user-attachments/assets/5b0fb715-47c3-43c2-9b74-b45afbf281d2">

#### Making PUT Request using different account for a different user -(b)
<img width="1019" alt="image" src="https://github.com/user-attachments/assets/aff3ddac-cf1f-442e-9be6-b7973217e928">

#### Making DELETE Request using different account for a different user 
<img width="1057" alt="image" src="https://github.com/user-attachments/assets/38a18463-1a9c-4ca0-96cf-9a8986d7aa81">



