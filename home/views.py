from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.
def index(request):
    # return HttpResponse("hello from index")
	result, params = ["Hello"], ["sel1", "sel2", "sel3"]
	if request.method == 'POST':
		for key in params:
			result.append(request.POST.get(key))

	result = "".join(result)
	return render(request, 'home/index.html',{'result': result})


def query1(request):
    return render(request, 'home/query1.html')

def about(request):
    return render(request, 'home/about.html')

def data_set(request):
    return render(request, 'home/data_set.html')

def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]
