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

query1_content = [ 
	{'title': 'Topics', 'fields': [], 'button_class':'btn btn-success disabled', 'button_title':'Next', 'save': ''},
	{'title': 'Questions', 'fields': [], 'button_class': 'btn btn-success disabled', 'button_title': 'Next', 'save':''},
	{'title': 'Indicator', 'fields': [], 'button_class': 'btn btn-success disabled', 'button_title': 'Next', 'save':''},
	{'title': 'Year', 'fields': [], 'button_class': 'btn btn-success disabled', 'button_title': 'Next', 'save':''},
	{ 'title': 'Above/Below', 'fields':[], 'button_class': 'btn btn-success disabled', 'button_title': 'Search', 'save':''}

]
def query1(request):
	global query1_content
	global ans1
	global ans2 
	global ans3
	global ans4
	global ans5
	ans, query_title = [], ""
	if ans1 == "":
		ans1 = "temp"
		query1_content[0]['fields'], query1_content[0]['button_class'] = populate_form('NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("Topics"):
		query1_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		query1_content[1]['fields'], query1_content[1]['button_class'] = populate_form('NAME', query)
	
	if request.method == 'POST' and request.POST.get("Questions"):
		query1_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		query1_content[2]['fields'], query1_content[2]['button_class'] = populate_form('DATA_VALUE_TYPE', query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query1_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select year_start from chronic_disease_indicator where name = '{}' order by year_start ASC".format(ans2)
		query1_content[3]['fields'], query1_content[3]['button_class'] = populate_form('YEAR_START', query)


	if request.method == 'POST' and request.POST.get("Year"):
		query1_content[3]['save'] = ans4 = request.POST.get("Year")
		query1_content[4]['fields'], query1_content[4]['button_class'] = ['above', 'below'], 'btn btn-success'

	if request.method == 'POST' and request.POST.get("Above/Below"):
		ans.extend([ans1, ans2, ans3, ans4, request.POST.get("Above/Below")])
		print(query_title)
		temp = ">" if request.POST.get("final") == "above" else "<"		

		query = """with temp_nat as (select * from indicator_estimate 
						where DATA_VALUE_TYPE = '{}' 
						and year_start = {} 
						and strat_id = 'OVR' 
						and indicator_id in (select indicator_id 
							from chronic_disease_indicator 
							where name = '{}')) select location.name, temp_nat.year_start as year, concat(round((select avg(data_value) 
								from temp_nat), 1), '%') as national_avg, 
								concat(temp_nat.data_value, temp_nat.data_unit) as location_data_value from temp_nat, location 
									where temp_nat.location_id = location.location_ID and temp_nat.data_value {} (select avg(data_value) from temp_nat)""".format(ans3, ans4, ans2, temp)
		query_title = query
		with connection.cursor() as cursor:
			cursor.execute(query)
			ans = dictfetchall(cursor)

		for i in query1_content:
			i['fields'], i['button_class'] = [], "btn btn-success disabled"

		ans1 = ans2 = ans3 = ans4 = ans5 = ""

	context = {
		'query1_content':query1_content,
		'ans' : (ans if ans else ""),
		'query_title' : query_title,
		'query_title': query_title,
		'ans1': (ans1 if ans1 else ""),
		'ans2': (ans2 if ans2 else ""),
		'ans3': (ans3 if ans3 else ""),
		'ans4': (ans4 if ans4 else "")
		
	}
	return render(request, 'home/query1.html', context)
	
questions_2, years_start_2, years_end_2, increase_decrease_2, indicator_2= [], [], [], [], []
question_button_2 = year_start_button_2 = year_end_button_2 = increase_decrease_button_2 = indicator_button_2= "btn btn-success disabled"
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
	global indicator_2
	global indicator_button_2
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
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		indicator_2, indicator_button_2 = populate_form('DATA_VALUE_TYPE', query)

	if request.method == 'POST' and request.POST.get("indicator"):
		ans3 = request.POST.get("indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(ans2)
		years_start_2, year_start_button_2 = populate_form('YEAR_START', query)

	if request.method == 'POST' and request.POST.get("years_start"):
		ans4 = request.POST.get("years_start")
		query = "select distinct year_end from chronic_disease_indicator where name = '{}' and year_end > {} order by year_end ASC".format(ans2, ans4)
		years_end_2, year_end_button_2 = populate_form('YEAR_END', query)

	if request.method == 'POST' and request.POST.get("years_end"):
		ans5 = request.POST.get("years_end")
		increase_decrease_2 = ["increase", "decrease"]
		increase_decrease_button_2 = "btn btn-success"
	
	if request.method == 'POST' and request.POST.get("final"):
		ans6 = request.POST.get("final")
		ans.extend([ans1, ans2, ans3, ans4, ans5, request.POST.get("final")])
		temp = "<" if ans6 == "increase" else ">"
		query = """With temp_nat as (select * from indicator_estimate 
					where DATA_VALUE_TYPE= '{}'
    		            and strat_id='OVR'
						and indicator_id in (select indicator_id from CHRONIC_DISEASE_INDICATOR
							where name='{}'))
							select location.name, t1.year_start as first_year, t1.data_value as first_value,
    				   			t2.year_start as second_year, t2.data_value as second_value
								from temp_nat t1,  temp_nat t2, location
									where t1.location_id = location.location_ID
										and t2.location_id = t1.location_id
    						  			and t1.year_start = {}
    						  			and t2.year_start = {}
    						  			and t1.data_value {} t2.data_value""".format(ans3, ans2, ans4, ans5, temp)

		query_title = query
		with connection.cursor() as cursor:
			cursor.execute(query)
			ans = dictfetchall(cursor)

		questions_2, years_start_2, years_end_2, increase_decrease_2, indicator_2 = [], [], [], [], []
		question_button_2 = years_start_button_2 = years_end_button_2 = increase_decrease_button_2 = indicator_button_2= "btn btn-success disabled"
		ans1 = ans2 = ans3 = ans3 = ans4 = ans5 = ans6 = ""
	
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
		'indicator' : indicator_2,
		'indicator_button': indicator_button_2
		
	}
	return render(request, 'home/query2.html', context)

questions_3, highest_lowest_3, population_3, indicator_3, years_3 = [], [], [], [], []
question_button_3 = highest_lowest_button_3 = population_button_3 = years_button_3 = indicator_button_3 = "btn btn-success disabled"
def query3(request):
	global health_domain
	global questions_3 
	global highest_lowest_3
	global question_button_3
	global highest_lowest_button_3
	global population_3
	global population_button_3
	global ans1
	global ans2 
	global ans3
	global ans4
	global ans5
	global ans6
	global years_3
	global years_button_3
	global indicator_3
	global indicator_button_3

	ans, query_title = [], ""
	
	health_domain, temp = populate_form('NAME', "Select distinct name from health_domain")
	if request.method == 'POST' and request.POST.get("topics"):
		ans1 = request.POST.get("topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		questions_3, question_button_3 = populate_form('NAME', query)

	if request.method == 'POST' and request.POST.get("questions"):
		ans2 = request.POST.get("questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(
			ans2)
		indicator_3, indicator_button_3 = populate_form('DATA_VALUE_TYPE', query)

	if request.method == 'POST' and request.POST.get("indicator"):
		ans3 = request.POST.get("indicator")
		print(ans3)
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(ans2)
		years_3, years_button_3 = populate_form('YEAR_START', query)

	if request.method == 'POST' and request.POST.get("years"):
		ans4 = request.POST.get("years")
		query = """ 
			select race as population from (
				(select distinct race, stratid from populationid)
				union (select distinct gender, stratid from populationid)
				union (select distinct overall, stratid from populationid))
			where race is not null and stratid in ( select stratid from indicator_estimate
													where data_value_type = '{}'
													and year_start = {}
													and indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}'))
		""".format(ans3, ans4, ans2)
		population_3, population_button_3 = populate_form('POPULATION', query)

	if request.method == 'POST' and request.POST.get("population"):
		ans5 = request.POST.get("population")
		highest_lowest_3 = ["highest", "lowest"]
		highest_lowest_button_3 = "btn btn-success"

	if request.method == 'POST' and request.POST.get("final"):
		ans6 = request.POST.get("final")
		ans.extend([ans1,ans2, ans3, request.POST.get("final")])
		temp = "desc" if ans6 == "highest" else "asc" 		
		query = """
			select * from (
			select location.name, temp_nat.data_value || temp_nat.data_unit as data_value
			from (select * from indicator_estimate  
						where DATA_VALUE_TYPE = '{}' 
								and strat_id in 
								(select STRATID from populationid where
										race = '{}' or 
										GENDER= '{}' or 
										OVERALL= '{}')
								and year_start = {}
								and indicator_id in (select indicator_id from CHRONIC_DISEASE_INDICATOR 
													where name = '{}')) temp_nat, location
						where temp_nat.location_id = location.location_ID
								and temp_nat.data_value is not null
						order by temp_nat.data_value {})
						where rownum < 11
		""".format(ans3, ans5, ans5, ans5, ans4, ans2, temp)
		
		with connection.cursor() as cursor:
			cursor.execute(query)
			ans = dictfetchall(cursor)

		questions_3, highest_lowest_3, years_3, indicator_3, population_3 = [], [], [], [], []
		ans1 = ans2 = asn3 = ans4 = ans5 = ans6 = ""
		question_button_3 = highest_lowest_button_3 = years_button_3 = indicator_button_3 = population_button_3 = "btn btn-success disabled"
	
	context = {
		'health_domain': health_domain,
		'questions': questions_3,
		'ans': (ans if ans else ""),
		'query_title': query_title,
		'question_button': question_button_3,
		'highest_lowest': highest_lowest_3,
		'highest_lowest_button': highest_lowest_button_3,
		'population_button' : population_button_3,
		'population' : population_3,
		'years': years_3,
		'year_button' : years_button_3,
		'indicator' : indicator_3,
		'indicator_button' : indicator_button_3
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
