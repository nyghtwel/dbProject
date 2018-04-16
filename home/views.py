from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.
def index(request):
	context = {}
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
	{'title': 'Above/Below', 'fields':[], 'button_class': 'btn btn-success disabled', 'button_title': 'Search', 'save':''}
]
def query1(request):
	global query1_content
	global ans1
	global ans2 
	global ans3
	global ans4
	global ans5
	ans, query_title, query = [], "", ""
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

		query_title = """with temp_nat as (select * from indicator_estimate 
						where DATA_VALUE_TYPE = '{}' 
						and year_start = {} 
						and strat_id = 'OVR' 
						and indicator_id in (select indicator_id 
							from chronic_disease_indicator 
							where name = '{}')) select location.name, temp_nat.year_start as year, concat(round((select avg(data_value) 
								from temp_nat), 1), '%') as national_avg, 
								concat(temp_nat.data_value, temp_nat.data_unit) as location_data_value from temp_nat, location 
									where temp_nat.location_id = location.location_ID and temp_nat.data_value {} (select avg(data_value) from temp_nat)
				""".format(ans3, ans4, ans2, temp)
		
		with connection.cursor() as cursor:
			cursor.execute(query_title)
			ans = dictfetchall(cursor)

		for i in query1_content:
			i['fields'], i['button_class'] = [], "btn btn-success disabled"

		ans1 = ans2 = ans3 = ans4 = ans5 = ""
		query1_content[0]['fields'], query1_content[0]['button_class'] = populate_form('NAME', "Select distinct name from health_domain")

	context = {
		'query1_content':query1_content,
		'ans' : (ans if ans else ""),
		'query_title' : query_title,
		'query_title': query_title,
		'ans1': (ans1 if ans1 else ""),
		'ans2': (ans2 if ans2 else ""),
		'ans3': (ans3 if ans3 else ""),
		'ans4': (ans4 if ans4 else ""), 
		'query': query
		
	}
	return render(request, 'home/query1.html', context)
	
query2_content = [
    {'title': 'Topics', 'fields': [], 'button_class': 'btn btn-success disabled','button_title': 'Next', 'save': ''},
	{'title': 'Questions', 'fields': [], 'button_class': 'btn btn-success disabled','button_title': 'Next', 'save': ''},
	{'title': 'Indicator', 'fields': [], 'button_class': 'btn btn-success disabled','button_title': 'Next', 'save': ''},
	{'title': 'Year_Start', 'fields': [], 'button_class': 'btn btn-success disabled','button_title': 'Next', 'save': ''},
   	{'title': 'Year_End', 'fields': [], 'button_class': 'btn btn-success disabled', 'button_title': 'Next', 'save': ''},
	{'title': 'Increase/Decrease', 'fields': [], 'button_class': 'btn btn-success disabled', 'button_title': 'Search', 'save': ''}
]
def query2(request):
	global query2_content
	global ans1
	global ans2
	global ans3
	global ans4
	global ans5

	ans, query_title, query = [], "", ""

	if ans1 == "":
		ans1 == "temp"
		query2_content[0]['fields'], query2_content[0]['button_class'] = populate_form('NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("Topics"):
		query2_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		query2_content[1]['fields'], query2_content[1]['button_class'] = populate_form('NAME', query)

	if request.method == 'POST' and request.POST.get("Questions"):
		query2_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		query2_content[2]['fields'], query2_content[2]['button_class'] = populate_form('DATA_VALUE_TYPE', query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query2_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(ans2)
		query2_content[3]['fields'], query2_content[3]['button_class'] = populate_form('YEAR_START', query)

	if request.method == 'POST' and request.POST.get("Year_Start"):
		query2_content[3]['save'] = ans4 = request.POST.get("Year_Start")
		query = "select distinct year_end from chronic_disease_indicator where name = '{}' and year_end > {} order by year_end ASC".format(ans2, ans4)
		query2_content[4]['fields'], query2_content[4]['button_class'] = populate_form('YEAR_END', query)

	if request.method == 'POST' and request.POST.get("Year_End"):
		query2_content[4]['save'] = ans5 = request.POST.get("Year_End")
		query2_content[5]['fields'], query2_content[5]['button_class'] = ['increase', 'decrease'], 'btn btn-success'
	
	if request.method == 'POST' and request.POST.get("Increase/Decrease"):
		ans6 = request.POST.get("final")
		ans.extend([ans1, ans2, ans3, ans4, ans5, request.POST.get("final")])
		temp = "<" if ans6 == "increase" else ">"
		query_title = """With temp_nat as (select * from indicator_estimate 
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
    						  			and t1.data_value {} t2.data_value
				""".format(ans3, ans2, ans4, ans5, temp)

		
		with connection.cursor() as cursor:
			cursor.execute(query_title)
			ans = dictfetchall(cursor)

		for i in query2_content:
			i['fields'], i['button_class'] = [], 'btn btn-success disabled'

		ans1 = ans2 = ans3 = ans3 = ans4 = ans5 = ans6 = ""
		query2_content[0]['fields'], query2_content[0]['button_class'] = populate_form(
			'NAME', "Select distinct name from health_domain")
	
	context = {
		'query2_content': query2_content,
		'ans': (ans if ans else ""),
		'query_title': query_title,
		'query' : query
		
	}
	return render(request, 'home/query2.html', context)

query3_content = [
    {'title': 'Topics', 'fields': [], 'button_class': 'btn btn-success disabled', 'button_title': 'Next', 'save': ''},
   	{'title': 'Questions', 'fields': [], 'button_class': 'btn btn-success disabled','button_title': 'Next', 'save': ''},
   	{'title': 'Indicator', 'fields': [], 'button_class': 'btn btn-success disabled','button_title': 'Next', 'save': ''},
   	{'title': 'Year', 'fields': [],'button_class': 'btn btn-success disabled', 'button_title': 'Next', 'save': ''},
   	{'title': 'Population', 'fields': [], 'button_class': 'btn btn-success disabled','button_title': 'Next', 'save': ''},
   	{'title': 'Highest/Lowest', 'fields': [],'button_class': 'btn btn-success disabled', 'button_title': 'Search', 'save': ''}
]
def query3(request):
	global query3_content
	global ans1
	global ans2 
	global ans3
	global ans4
	global ans5
	global ans6

	ans, query_title, query = [], "", ""
	
	if ans1 == "":
		ans1 == "temp"
		query3_content[0]['fields'], query3_content[0]['button_class'] = populate_form('NAME', "Select distinct name from health_domain")
	
	if request.method == 'POST' and request.POST.get("Topics"):
		query3_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		query3_content[1]['fields'], query3_content[1]['button_class'] = populate_form('NAME', query)

	if request.method == 'POST' and request.POST.get("Questions"):
		query3_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		query3_content[2]['fields'], query3_content[2]['button_class'] = populate_form(
			'DATA_VALUE_TYPE', query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query3_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(ans2)
		query3_content[3]['fields'], query3_content[3]['button_class'] = populate_form(
			'YEAR_START', query)

	if request.method == 'POST' and request.POST.get("Year"):
		query3_content[3]['save'] = ans4 = request.POST.get("Year")
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
		query3_content[4]['fields'], query3_content[4]['button_class'] = populate_form('POPULATION', query)

	if request.method == 'POST' and request.POST.get("Population"):
		query3_content[4]['save'] = ans5 = request.POST.get("Population")
		query3_content[5]['fields'], query3_content[5]['button_class'] = ["highest", "lowest"], "btn btn-success"

	if request.method == 'POST' and request.POST.get("Highest/Lowest"):
		query3_content[5]['save'] =	ans6 = request.POST.get("Highest/Lowest")
		temp = "desc" if ans6 == "highest" else "asc" 		
		query_title = """
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
			cursor.execute(query_title)
			ans = dictfetchall(cursor)

		for i in query3_content:
			i['fields'], i['button_class'], i['save'] = [], "btn btn-success disabled", ''

		query3_content[0]['fields'], query3_content[0]['button_class'] = populate_form('NAME', "Select distinct name from health_domain")
		ans1 = ans2 = asn3 = ans4 = ans5 = ans6 = ""
	
	context = {
		'query3_content': query3_content,
		'ans': (ans if ans else ""),
		'query_title': query_title,
		'query' : query
	}
	return render(request, 'home/query3.html', context)

query4_content = [
    {'title': 'Topics', 'fields': [], 'button_class': 'btn btn-success disabled', 'button_title': 'Next', 'save': ''},
   	{'title': 'Questions', 'fields': [], 'button_class': 'btn btn-success disabled','button_title': 'Next', 'save': ''},
   	{'title': 'Indicator', 'fields': [], 'button_class': 'btn btn-success disabled','button_title': 'Next', 'save': ''},
   	{'title': 'Year Start', 'fields': [],'button_class': 'btn btn-success disabled', 'button_title': 'Next', 'save': ''},
   	{'title': 'Year End', 'fields': [], 'button_class': 'btn btn-success disabled','button_title': 'Next', 'save': ''},
   	{'title': 'Increase/Decrease', 'fields': [],'button_class': 'btn btn-success disabled', 'button_title': 'Search', 'save': ''}
]
def query4(request):
	global query4_content
	global ans1 
	global ans2
	global ans3
	global ans4 
	global ans5
	ans, query_title, query = [], "", ""

	if ans1 == "":
		ans1 == "temp"
		query4_content[0]['fields'], query4_content[0]['button_class'] = populate_form('NAME', "Select distinct name from health_domain")
	
	if request.method == 'POST' and request.POST.get("Topics"):
		query4_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		query4_content[1]['fields'], query4_content[1]['button_class'] = populate_form('NAME', query)

	if request.method == 'POST' and request.POST.get("Questions"):
		query4_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		query4_content[2]['fields'], query4_content[2]['button_class'] = populate_form('DATA_VALUE_TYPE', query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query4_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(ans2)
		query4_content[3]['fields'], query4_content[3]['button_class'] = populate_form('YEAR_START', query)

	if request.method == 'POST' and request.POST.get("Year Start"):
		query4_content[3]['save'] = ans4 = request.POST.get("Year Start")
		query = "select distinct year_end from chronic_disease_indicator where year_end > {} order by year_end ASC".format(ans4)
		query4_content[4]['fields'], query4_content[4]['button_class'] = populate_form('YEAR_END', query)
	
	if request.method == 'POST' and request.POST.get("Year End"):
		query4_content[4]['save'] = ans5 = request.POST.get("Year End")
		query4_content[5]['fields'], query4_content[5]['button_class'] = ["increase", "decrease"], "btn btn-success"

	if request.method == 'POST' and request.POST.get("Increase/Decrease"):
		query4_content[5]['save'] = request.POST.get("Increase/Decrease")
		topic, question, indicator, y1, y2 = ans1, ans2, ans3, ans4, ans5
		temp = "<" if query4_content[5]['save'] == "increase" else ">"
		query_title = """
			select id1 as question, round(dat_val1 , 3)as avg_val_year1, round(dat_val2 , 3) as avg_val_year2 from (
					select health_domain.name as name1,
					chronic_disease_indicator.name as id1, 
					indicator_estimate.DATA_VALUE_TYPE as type1,
					avg(INDICATOR_ESTIMATE.data_value) as dat_val1
					from indicator_estimate, chronic_disease_indicator, health_domain where 
					indicator_estimate.indicator_id = chronic_disease_indicator.indicator_id and
					health_domain.domain_id = chronic_disease_indicator.domain_id and 
					health_domain.name = '{}' and
					indicator_estimate.year_start = '{}' and
					data_value_type = '{}' and
					data_value is not null and
					strat_id = 'OVR'
					group by health_domain.name, chronic_disease_indicator.name, indicator_estimate.DATA_VALUE_TYPE
					),
					(select health_domain.name as name2,
					chronic_disease_indicator.name as id2, 
					indicator_estimate.DATA_VALUE_TYPE as type2,
					avg(INDICATOR_ESTIMATE.data_value) as dat_val2
					from indicator_estimate, chronic_disease_indicator, health_domain where 
					indicator_estimate.indicator_id = chronic_disease_indicator.indicator_id and
					health_domain.domain_id = chronic_disease_indicator.domain_id and 
					health_domain.name = '{}' and
					indicator_estimate.year_start = '{}' and
					data_value_type = '{}' and
					data_value is not null and
					strat_id = 'OVR'
					group by health_domain.name, chronic_disease_indicator.name, indicator_estimate.DATA_VALUE_TYPE)
					
			where  name1 = name2 and
			id1 = id2 and
			type1 = type2 and
			dat_val2 {} dat_val1
			""".format(topic, y1, indicator, topic, y2, indicator, temp)
		
		
		with connection.cursor() as cursor:
			cursor.execute(query_title)
			ans = dictfetchall(cursor)

		for i in query4_content:
			i['fields'], i['button_class'] = [], "btn btn-success disabled"

		query4_content[0]['fields'], query4_content[0]['button_class'] = populate_form('NAME', "Select distinct name from health_domain")
		ans1 = ans2 = asn3 = ans4 = ans5 = ""

	context = {
		'query4_content' : query4_content,
		'ans' : (ans if ans else ""),
		'query_title': query_title,
	}
	return render(request, 'home/query4.html', context)

questions_5, indicator_5, increase_decrease_5 = [], [], []
question_button_5 = indicator_button_5 = increase_decrease_button_5 = "btn btn-success disabled"
def query5(request):
	global health_domain
	global questions_5
	global question_button_5
	global increase_decrease_5
	global increase_decrease_button_5
	global indicator_5
	global indicator_button_5
	global ans1
	global ans2
	global ans3

	ans, query_title = [], ""

	if ans1 == "":
		ans1 = request.POST.get("topics")
		print(ans1)
		health_domain, temp = populate_form('NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("topics"):
		ans1 = request.POST.get("topics")
		ans2 = request.POST.get("questions")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		questions_5, question_button_5 = populate_form('NAME', query)

	if request.method == 'POST' and request.POST.get("questions"):
		ans2 = request.POST.get("questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		indicator_5, indicator_button_5 = populate_form('DATA_VALUE_TYPE', query)

	if request.method == 'POST' and request.POST.get("final"):
		ans.extend([ans1,ans2,request.POST.get("final")])
		questions_5 = indicator_5 = increase_decrease_5 = []
		question_button_5 = indicator_button_5 = increase_decrease_button_5 = "btn btn-success disabled"
		ans1 = ans2 = ""

	context = {
		'health_domain' : health_domain,
		'questions' : questions_5,
		'question_button' : question_button_5,
		'increase_decrease' : increase_decrease_5,
		'increase_decrease_button' : increase_decrease_button_5,
		'ans' : (ans if ans else ""),
		'query_title' : query_title,
		'indicator' : indicator_5,
		'indicator_button' : indicator_button_5
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
