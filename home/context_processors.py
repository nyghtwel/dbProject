from django.conf import settings
def user_name(request):
    
    return {'user_name' : settings.USER_NAME}

def user(request):

    return {'user': settings.USER}