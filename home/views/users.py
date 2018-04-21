from django.shortcuts import render
from .helper import *

def user(request):
    # add_user()
    # get_user()
    # show_user()
    # update_user()
    # delete_user()
    # show_user_history()
    context = {

    }
    return render(request, 'home/user.html', context)

def add_user():
    pass 

def get_user():
    pass 

def show_user():
    pass

def update_user(parameter_list):
    pass

def delete_user(parameter_list):
    pass

def show_user_history(parameter_list):
    pass


