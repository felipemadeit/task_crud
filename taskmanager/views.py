from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login, logout
from django.db import IntegrityError

def home_view (request):
    return render(request, 'home.html')

def signup (request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:   
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
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
    return render (request, 'task.html')

def log_out (request):
    logout(request)
    return redirect('home')