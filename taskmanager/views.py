from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task

def home_view (request):
    # Principal view
    return render(request, 'home.html')

def signup (request):
    # Sign Up view
    # If the method if get return a form to cath the user data
    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
        })
    else:
        # If the method is not get is a post method
        # Validate if the passwords match 
        if request.POST['password1'] == request.POST['password2']:
            # Try to create a user with the user data and save it
            try:   
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # Create a session to the user registered
                login(request, user)
                # Redirect to the task view
                return redirect('task')
            # try to catch the integrity error
            # The integrity error is when the user try to sign up but he is already created
            except IntegrityError:
                return render(request, 'login.html', {
                    'form': UserCreationForm,
                    'error': 'Username Already Exists'

                })
        else:
            return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Password do not match'
            })


def task_view (request):
    tasks = Task.objects.filter(user=request.user)
    return render (request, 'task.html', {
        'tasks': tasks
    })

def log_out (request):
    logout(request)
    return redirect('home')

def log_in (request):
    if request.method == 'GET':
        return render(request, 'login.html',  {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error' : 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('/task')
        
def create_task (request):

    if request.method == 'GET':

        return render(request, 'create_task.html', {

            'form' : TaskForm
        })
    
    else: 
        try: 

            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task')
        
        except ValueError:

            return render (request, 'create_task.html', {
                'form' : TaskForm,
                'error': 'Please enter valid data'
        })