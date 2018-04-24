from django.shortcuts import render
from .helper import *
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.conf import settings
def users(request):
    # add_user()
    # get_user()
    # show_user()
    # update_user()
    # delete_user()
    # show_user_history()
    response = HttpResponse()
    
    if request.POST:
        print('in post')

        options = ['sign up', 'login', 'logout']
        for option in options:
            if request.POST.get(option):
                print(option)
                next = request.POST.get(option, '/')
                if option == 'sign up': 
                    add_user(request)
                if option == 'login':
                    settings.USER = True
                if option == 'logout': 
                    logout_user(request)
                return HttpResponseRedirect(next)
        
        
    context = {

    }
    return render(request, 'home/users.html', context)

def add_user(request):
    print('user')
    # user = User.objects.create_user(username='test2', password='password') 
    # print(user)

def get_user(request):
    user = authenticate(request, username='test', password='dummy')
    # login(user)
    print('login')

def show_user():
    pass

def update_user(parameter_list):
    pass

def delete_user(parameter_list):
    pass

def show_user_history(parameter_list):
    pass

def logout_user(request):
    print('logout')
    # logout(request)
