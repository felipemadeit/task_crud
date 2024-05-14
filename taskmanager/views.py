from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

def home_view (request):
    return render(request, 'home.html')

def signup (request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try :   
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return HttpResponse('User created succesfully!')
                # Register User
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username Already Exists'
                })
        else:
            return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Password do not match'
            })


    
