from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("hello from index")
    return render(request, 'home/index.html')


def query1(request):
    return render(request, 'home/query1.html')

def about(request):
    return render(request, 'home/about.html')

def data_set(request):
    return render(request, 'home/data_set.html')