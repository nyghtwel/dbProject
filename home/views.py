from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.
def index(request):
    # return HttpResponse("hello from index")
	result, params = [], ["sel1", "sel2", "sel3"]
	title, rows = "", []
	if request.method == 'POST':
		# title = "Select * from chronic"
		title = "Basic query with {}, {}, and {}".format(request.POST.get("sel1"), request.POST.get("sel2"), request.POST.get("sel3"))
		with connection.cursor() as cursor:
			# query = "Select * from GEO_LAKE"
			query = "Select * from chronic_disease_indicator"
			cursor.execute(query)
			rows = dictfetchall(cursor)		

		for key in params:
			result.append(request.POST.get(key))


	result = "".join(result)
	context = {
		'result': result,
		'title': title,
		'rows': rows
	}
	return render(request, 'home/index.html', context)


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
