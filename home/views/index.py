from .helper import *

def index(request):
	query = '''with temp_count as
			((select count(rowid)as number_of_rows from CHRONIC_DISEASE_INDICATOR) union
 			(select count(rowid) as number_of_rows from INDICATOR_ESTIMATE) union
 			(select count(rowid) as number_of_rows from POPULATIONID) union
 			(select count(rowid) as number_of_rows from HEALTH_DOMAIN) union
 			(select count(rowid) as number_of_rows from location))
			select sum(number_of_rows) as total_no_of_tuples from temp_count
			'''
	total = ""
	if request.method == 'POST' and request.POST.get('submit'):
		with connection.cursor() as cursor:
				cursor.execute(query)
				total = dictfetchall(cursor)[0]['TOTAL_NO_OF_TUPLES']

	messages.success(request, query)
	context = {
		'total': total
	}
	return render(request, 'home/index.html', context)
