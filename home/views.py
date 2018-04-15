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
		# title = "Basic query with {}, {}, and {}".format(request.POST.get("sel1"), request.POST.get("sel2"), request.POST.get("sel3"))
		with connection.cursor() as cursor:
			# query = "Select * from GEO_LAKE"
			query = "Select distinct name from Health_Domain"
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


ans1 = ans2 = ans3 = ans4 = ans5 = ans6 = ""
def populate_form(id, query):
	table = []
	with connection.cursor() as cursor:
			cursor.execute(query)
			table = dictfetchall(cursor)
			# print(table)
			table = [row[id] for row in table]

	return (table, "btn btn-success")

health_domain, questions_1, years_1, above_below_1, indicator_1= [], [], [], [], []
indicator_button_1 = question_button_1 = year_button_1  = above_below_button_1 = increase_decrease_button_1 = "btn btn-success disabled"
def query1(request):
	global health_domain
	global questions_1
	global years_1
	global above_below_1
	global question_button_1
	global year_button_1
	global above_below_button_1
	global indicator_1
	global indicator_button_1
	global ans1
	global ans2 
	global ans3
	global ans4
	global ans5
	ans, query_title = [], ""

	if ans1 == "":
		ans1 = request.POST.get("topics")
		print(ans1)
		health_domain, temp = populate_form('NAME', "Select distinct name from health_domain")
	
	if request.method == 'POST' and request.POST.get("topics"):
		ans1 = request.POST.get("topics")
		ans2 = request.POST.get("questions")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		questions_1, question_button_1 = populate_form('NAME', query)
	
	if request.method == 'POST' and request.POST.get("questions"):
		ans2 = request.POST.get("questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		indicator_1, indicator_button_1 = populate_form('DATA_VALUE_TYPE', query)

	if request.method == 'POST' and request.POST.get("indicator"):
		ans3 = request.POST.get("indicator")
		query = "select year_start from chronic_disease_indicator where name = '{}' order by year_start ASC".format(ans2)
		years_1, year_button_1 = populate_form('YEAR_START', query)


	if request.method == 'POST' and request.POST.get("years"):
		ans4 = request.POST.get("years")
		above_below_1 = ["above", "below"]
		above_below_button_1 = "btn btn-success"


	if request.method == 'POST' and request.POST.get("final"):
		ans.extend([ans1, ans2, ans3, ans4, request.POST.get("final")])
		print(query_title)
		temp = ">" if request.POST.get("final") == "above" else "<"		

		query = "with temp_nat as (select * from indicator_estimate where DATA_VALUE_TYPE = '{}' and year_start = {} and strat_id = 'OVR' and indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')) select location.name, temp_nat.year_start as year, concat(round((select avg(data_value) from temp_nat), 1), '%') as national_avg, concat(temp_nat.data_value, temp_nat.data_unit) as location_data_value from temp_nat, location where temp_nat.location_id = location.location_ID and temp_nat.data_value {} (select avg(data_value) from temp_nat)".format(ans3, ans4, ans2, temp)
		query_title = query
		with connection.cursor() as cursor:
			cursor.execute(query)
			ans = dictfetchall(cursor)

		questions_1, years_1, above_below_1, indicator_1 = [], [], [], []
		question_button_1 = year_button_1 = above_below_button_1 = indicator_button_1 = "btn btn-success disabled"
		ans1 = ans2 = ans3 = ans4 = ans5 = ""

	context = {
		'health_domain': health_domain,
		'questions' : questions_1,
		'years' : years_1,
		'above_below' : above_below_1,
		'ans' : (ans if ans else ""),
		'query_title' : query_title,
		'question_button' : question_button_1,
		'year_button' : year_button_1,
		'above_below_button' : above_below_button_1,
		'indicator' : indicator_1,
		'indicator_button' : indicator_button_1,
		'query_title': query_title,
		'ans1': (ans1 if ans1 else ""),
		'ans2': (ans2 if ans2 else ""),
		'ans3': (ans3 if ans3 else ""),
		'ans4': (ans4 if ans4 else "")
		
	}
	return render(request, 'home/query1.html', context)
	
questions_2, years_start_2, years_end_2, increase_decrease_2 = [], [], [], []
question_button_2 = year_start_button_2 = year_end_button_2 = increase_decrease_button_2 = "btn btn-success disabled"
def query2(request):
	global health_domain
	global questions_2
	global years_start_2
	global years_end_2
	global question_button_2
	global year_start_button_2
	global year_end_button_2
	global increase_decrease_2
	global increase_decrease_button_2
	global ans1
	global ans2
	global ans3
	global ans4
	global ans5

	ans, query_title = [], ""

	health_domain, temp = populate_form('NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("topics"):
		ans1 = request.POST.get("topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		questions_2, question_button_2 = populate_form('NAME', query)

	if request.method == 'POST' and request.POST.get("questions"):
		ans2 = request.POST.get("questions")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(ans2)
		years_start_2, year_start_button_2 = populate_form('YEAR_START', query)

	if request.method == 'POST' and request.POST.get("years_start"):
		ans3 = request.POST.get("years_start")
		query = "select distinct year_end from chronic_disease_indicator where name = '{}' and year_end > {} order by year_end ASC".format(ans2, ans3)
		years_end_2, year_end_button_2 = populate_form('YEAR_END', query)

	if request.method == 'POST' and request.POST.get("years_end"):
		ans4 = request.POST.get("years_end")
		increase_decrease_2 = ["increase", "decrease"]
		increase_decrease_button_2 = "btn btn-success"
	
	if request.method == 'POST' and request.POST.get("final"):
		ans.extend([ans1, ans2, ans3, ans4, request.POST.get("final")])
		questions_2, years_start_2, years_end_2, increase_decrease_2 = [], [], [], []
		question_button_2 = years_start_button_2 = years_end_button_2 = increase_decrease_button_2 = "btn btn-success disabled"
		ans1 = ans2 = ans3 = ans3 = ""
	
	context = {
		'health_domain': health_domain,
		'questions': questions_2,
		'years_start': years_start_2,
		'years_end': years_end_2,
		'ans': (ans if ans else ""),
		'query_title': query_title,
		'question_button': question_button_2,
		'year_start_button': year_start_button_2,
		'year_end_button' : year_end_button_2,
		'increase_decrease' : increase_decrease_2,
		'increase_decrease_button': increase_decrease_button_2,
		
	}
	return render(request, 'home/query2.html', context)

questions_3, highest_lowest_3 = [], []
question_button_3 = highest_lowest_button_3 = "btn btn-success disabled"
def query3(request):
	global health_domain
	global questions_3 
	global highest_lowest_3
	global question_button_3
	global highest_lowest_button_3
	global ans1
	global ans2 


	ans, query_title = [], ""

	health_domain, temp = populate_form('NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("topics"):
		ans1 = request.POST.get("topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		questions_3, question_button_3 = populate_form('NAME', query)

	if request.method == 'POST' and request.POST.get("questions"):
		ans2 = request.POST.get("questions")
		highest_lowest_3 = ["highest", "lowest"]	
		highest_lowest_button_3 = "btn btn-success"
	
	if request.method == 'POST' and request.POST.get("final"):
		ans.extend([ans1,ans2, request.POST.get("final")])		
		questions_3, highest_lowest_3 = [], []
		question_button_3 = highest_lowest_button_3 = "btn btn-success disabled"
	
	context = {
		'health_domain': health_domain,
		'questions': questions_3,
		'ans': (ans if ans else ""),
		'query_title': query_title,
		'question_button': question_button_3,
		'highest_lowest': highest_lowest_3,
		'highest_lowest_button': highest_lowest_button_3
	}
	return render(request, 'home/query3.html', context)

years_start_4, years_end_4, increase_decrease_4 = [], [], []
year_start_button_4 = year_end_button_4 = increase_decrease_button_4 = "btn btn-success disabled"
def query4(request):
	global years_start_4
	global years_end_4 
	global year_start_button_4
	global year_end_button_4
	global increase_decrease_4
	global increase_decrease_button_4
	global ans1 
	global ans2
	global ans3

	ans, query_title = [], ""

	if not request.POST.get("years_end") or not request.POST.get("final"):
		years_start_4, year_start_button_4 = populate_form('YEAR_START', "select distinct year_start from chronic_disease_indicator where year_start >= 2007 order by year_start ASC")

	if request.method == 'POST' and request.POST.get("years_start"):
		ans1 = request.POST.get("years_start")
		query = "select distinct year_end from chronic_disease_indicator where year_end > {} order by year_end ASC".format(ans1)
		years_end_4, year_end_button_4 = populate_form('YEAR_END', query)
	
	if request.method == 'POST' and request.POST.get("years_end"):
		ans2 = request.POST.get("years_end")
		increase_decrease_4 = ["increase", "decrease"]
		increase_decrease_button_4 = "btn btn-success"

	if request.method == 'POST' and request.POST.get("final"):
		ans.extend([ans1,ans2,request.POST.get("final")])
		years_end_4, increase_decrease_4 = [], []
		year_start_button_4 = year_end_button_4 = increase_decrease_button_4 = "btn btn-success disabled"
		ans1 = ans2 = ""

	context = {
		'years_start' : years_start_4,
		'years_end' : years_end_4,
		'year_start_button' : year_start_button_4,
		'year_end_button' : year_end_button_4,
		'ans' : (ans if ans else ""),
		'query_title': query_title,
		'increase_decrease' : increase_decrease_4,
		'increase_decrease_button' : increase_decrease_button_4
	}
	return render(request, 'home/query4.html', context)

def query5(request):
	context = {

	}
	return render(request, 'home/query5.html', context)
	
def about(request):
	context = {

	}
	return render(request, 'home/about.html', context)
	
	
def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]
