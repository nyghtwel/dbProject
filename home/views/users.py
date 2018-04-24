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
                msg = ""
                if option == 'sign up': 
                    username = request.POST.get('user')
                    password = request.POST.get('pwd')
                    if add_user(username, password): 
                        msg = 'User added'
                        settings.USER = True
                        settings.USER_NAME = username
                    else: msg = 'Failed to add user'
                    print(msg)

                if option == 'login':
                    print('login')
                    print(request.POST)
                    username = request.POST.get('user')
                    password = request.POST.get('pwd')
                    if (validate_login(username, password)):
                        msg = 'Login successful'                      
                        settings.USER = True
                        settings.USER_NAME = username
                    else:
                        msg = 'Failed to login'

                if option == 'logout': 
                    settings.USER = False
                    msg = 'Logged out'
                
                messages.success(request, msg)
                return HttpResponseRedirect(next)
        
    user_history = show_user_history(settings.USER_NAME)
    print(user_history)
    context = {
        'user_history': user_history
    }
    return render(request, 'home/users.html', context)

def add_user(username, password):
    
    if not validate_username(username): return False
    query = '''insert into users(username, password) values('{}', '{}')
    '''.format(username, password)

    with connection.cursor() as cursor:
        cursor.execute(query)
    return True
    # user = User.objects.create_user(username='test2', password='password') 
    # print(user)


def validate_username(input):
    query = ''' select username from users where username = '{}'
        '''. format(input)
    ans = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        ans = cursor.fetchone()
    
    print(ans)
    if ans == input: return False
    else: return True

def validate_login(username, password):
    query = ''' select username from users where username = '{}' and password = '{}' 
            '''. format(username, password)
    ans = None
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        ans = cursor.fetchone()
    print('validate login')
    print(ans)   
    if ans: return True
    else: return False     
     
def show_user_history(username):
    # if request.method == 'POST' and request.POST.get('submit'):

    query = '''select write.username, write.datetime, query.query from query, write 
            where query.query_id = write.query_id and 
            write.username ='{}' 
            '''.format(username)
    
    ans = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        ans = dictfetchall(cursor)
    
    return ans


