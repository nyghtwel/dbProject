from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.contrib import messages
# Create your views here.
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
				
	context = {
		'total' : total
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

	return (table, "")

query1_content = [ 
	{'title': 'Topics', 'fields': [], 'disabled':'disabled', 'save': ''},
	{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Year', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Above/Below', 'fields':[], 'disabled': 'disabled', 'save':''}
]
def query1(request):
	global query1_content
	global ans1 
	global ans2 
	global ans3
	global ans4 
	btn_class = 'btn btn-success disabled'
	ans, query_title, query = [], "", ""
	# if ans1 == "":
		# ans1 = "temp"
	for i in query1_content:
		if i['fields']: i['fields'].pop(0)

	query1_content[0]['fields'], query1_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")
	
	if request.method == 'POST' and request.POST.get("Topics"):
		query1_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		for i in query1_content[1:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		query1_content[1]['fields'], query1_content[1]['disabled'] = populate_form('NAME', query)
		for i in query1_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Questions"):
		query1_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		for i in query1_content[2:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		query1_content[2]['fields'], query1_content[2]['disabled'] = populate_form('DATA_VALUE_TYPE', query)
		for i in query1_content[3:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query1_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select year_start from chronic_disease_indicator where name = '{}' order by year_start ASC".format(ans2)
		for i in query1_content[3:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		query1_content[3]['fields'], query1_content[3]['disabled'] = populate_form('YEAR_START', query)
		messages.success(request, query)		
	
		for i in query1_content[4:]:
			i['disabled'] = 'disabled'

	if request.method == 'POST' and request.POST.get("Year"):
		query1_content[3]['save'] = ans4 = request.POST.get("Year")
		
		for i in query1_content[4:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		
		query1_content[4]['fields'], query1_content[4]['disabled'] = ['above', 'below'], ''
		
		for i in query1_content[5:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Above/Below"):
		query1_content[4]['save'] = request.POST.get("Above/Below")
		btn_class = 'btn btn-success'

	if request.method == 'POST' and request.POST.get("submit"):
		print("here")
		temp = ">" if query1_content[4]['save'] == "above" else "<"		
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

		messages.success(request, query_title)
		
		for i in query1_content:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""

		ans1 = ans2 = ans3 = ans4 = ans5 = ""
		query1_content[0]['fields'], query1_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")

	for i in query1_content:
		i['fields'].insert(0, i['save'])

	# print(request.session.get('topic'))	
	context = {
		'query1_content':query1_content,
		'ans' : (ans if ans else ""),
		'ans1': (ans1 if ans1 else ""),
		'ans2': (ans2 if ans2 else ""),
		'ans3': (ans3 if ans3 else ""),
		'ans4': (ans4 if ans4 else ""), 
		
		'btn_class' : btn_class
		
	}
	return render(request, 'home/query1.html', context)
	
query2_content = [
    {'title': 'Topics', 'fields': [], 'disabled': 'disabled', 'save': ''},
	{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save': ''},
	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save': ''},
	{'title': 'Year_Start', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Year_End', 'fields': [], 'disabled': 'disabled', 'save': ''},
	{'title': 'Increase/Decrease', 'fields': [], 'disabled': 'disabled', 'save': ''}
]
def query2(request):
	global query2_content
	global ans1 
	global ans2 
	global ans3 
	global ans4 
	global ans5 
	btn_class = 'btn btn-success disabled'

	for i in query2_content:
		if i['fields']: i['fields'].pop(0)

	ans, query_title, query = [], "", ""

	# if ans1 == "":
	ans1 == ""
	query2_content[0]['fields'], query2_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("Topics"):
		query2_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		query2_content[1]['fields'], query2_content[1]['disabled'] = populate_form('NAME', query)
		for i in query2_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Questions"):
		query2_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		query2_content[2]['fields'], query2_content[2]['disabled'] = populate_form('DATA_VALUE_TYPE', query)
		for i in query2_content[3:]:
			i['disabled'] = 'disabled'
		
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query2_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 and year_start < (select max(year_end) from chronic_disease_indicator where name = '{}' ) order by year_start ASC".format(ans2,ans2)
		query2_content[3]['fields'], query2_content[3]['disabled'] = populate_form('YEAR_START', query)
		for i in query2_content[4:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year_Start"):
		query2_content[3]['save'] = ans4 = request.POST.get("Year_Start")
		query = "select distinct year_end from chronic_disease_indicator where name = '{}' and year_end > {} order by year_end ASC".format(ans2, ans4)
		query2_content[4]['fields'], query2_content[4]['disabled'] = populate_form('YEAR_END', query)
		for i in query2_content[5:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year_End"):
		query2_content[4]['save'] = ans5 = request.POST.get("Year_End")
		query2_content[5]['fields'], query2_content[5]['disabled'] = ['increase', 'decrease'], ''
		for i in query2_content[6:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Increase/Decrease"):
		query2_content[5]['save'] = ans6 = request.POST.get("Increase/Decrease")
		btn_class = 'btn btn-success'
		
	if request.method == 'POST' and request.POST.get("submit"):
		temp = "<" if query2_content[5]['save'] == "increase" else ">"
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
		messages.success(request, query_title)

		for i in query2_content:
			i['fields'], i['disabled'], i['save'] = [], 'disabled', ''

		ans1 = ans2 = ans3 = ans3 = ans4 = ans5 = ans6 = ""
		query2_content[0]['fields'], query2_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")

	for i in query2_content:
		if i['fields']: i['fields'].insert(0, i['save'])

	context = {
		'query2_content': query2_content,
		'ans': (ans if ans else ""),
		
		
		'btn_class' : btn_class
	}
	return render(request, 'home/query2.html', context)

query3_content = [
    {'title': 'Topics', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Year', 'fields': [],'disabled': 'disabled', 'save': ''},
   	{'title': 'Population', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Highest/Lowest', 'fields': [],'disabled': 'disabled', 'save': ''}
]

def query3(request):
	global query3_content
	global ans1
	global ans2 
	global ans3 
	global ans4 
	global ans5 
	global ans6
	btn_class = 'btn btn-success disabled'
	ans, query_title, query = [], "", ""

	for i in query3_content:
		if i['fields']: i['fields'].pop(0)

	query3_content[0]['fields'], query3_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")
	
	if request.method == 'POST' and request.POST.get("Topics"):
		query3_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		query3_content[1]['fields'], query3_content[1]['disabled'] = populate_form('NAME', query)
		for i in query3_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Questions"):
		query3_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		query3_content[2]['fields'], query3_content[2]['disabled'] = populate_form('DATA_VALUE_TYPE', query)
		for i in query3_content[3:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query3_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(ans2)
		query3_content[3]['fields'], query3_content[3]['disabled'] = populate_form('YEAR_START', query)
		for i in query3_content[4:]:
			i['disabled'] = 'disabled'

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
		query3_content[4]['fields'], query3_content[4]['disabled'] = populate_form('POPULATION', query)
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Population"):
		query3_content[4]['save'] = ans5 = request.POST.get("Population")
		query3_content[5]['fields'], query3_content[5]['disabled'] = ["highest", "lowest"], "btn btn-success"
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Highest/Lowest"):
		query3_content[5]['save'] =	ans6 = request.POST.get("Highest/Lowest")
		btn_class = 'btn btn-success'

	if request.method == 'POST' and request.POST.get('submit'):
		temp = "desc" if query3_content[5]['save'] == "highest" else "asc" 		
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
		messages.success(request, query_title)
		for i in query3_content:
			i['fields'], i['disabled'], i['save'] = [], "btn btn-success disabled", ''

		query3_content[0]['fields'], query3_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")
		ans1 = ans2 = asn3 = ans4 = ans5 = ans6 = ""

	for i in query3_content:
		i['fields'].insert(0, i['save'])

	context = {
		'query3_content': query3_content,
		'ans': (ans if ans else ""),
		
		
		'btn_class' : btn_class
	}
	return render(request, 'home/query3.html', context)

query4_content = [
    {'title': 'Topics', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Year Start', 'fields': [],'disabled': 'disabled', 'save': ''},
   	{'title': 'Year End', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Increase/Decrease', 'fields': [],'disabled': 'disabled', 'save': ''}
]
def query4(request):
	global query4_content
	global ans1
	global ans2
	global ans3
	global ans4
	global ans5
	ans, query_title, query = [], "", ""

	btn_class = 'btn btn-success disabled'
	for i in query4_content:
		if i['fields']: i['fields'].pop(0)

	ans1 == ""

	query4_content[0]['fields'], query4_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")
	
	if request.method == 'POST' and request.POST.get("Topics"):
		query4_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		query4_content[1]['fields'], query4_content[1]['disabled'] = populate_form('NAME', query)
		for i in query4_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Questions"):
		query4_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		query4_content[2]['fields'], query4_content[2]['disabled'] = populate_form('DATA_VALUE_TYPE', query)
		for i in query4_content[3:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query4_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(ans2)
		query4_content[3]['fields'], query4_content[3]['disabled'] = populate_form('YEAR_START', query)
		for i in query4_content[4:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year Start"):
		query4_content[3]['save'] = ans4 = request.POST.get("Year Start")
		query = "select distinct year_end from chronic_disease_indicator where year_end > {} order by year_end ASC".format(ans4)
		query4_content[4]['fields'], query4_content[4]['disabled'] = populate_form('YEAR_END', query)
		for i in query4_content[5:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year End"):
		query4_content[4]['save'] = ans5 = request.POST.get("Year End")
		query4_content[5]['fields'], query4_content[5]['disabled'] = ["increase", "decrease"], "btn btn-success"
		for i in query4_content[6:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Increase/Decrease"):
		query4_content[5]['save'] = request.POST.get("Increase/Decrease")
		btn_class = 'btn btn-success'
	
	if request.method == 'POST' and request.POST.get('submit'):
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
			i['fields'], i['disabled'], i['save'] = [], "disabled", ''

		messages.success(request, query_title)
		
		query4_content[0]['fields'], query4_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")
		ans1 = ans2 = asn3 = ans4 = ans5 = ""

	for i in query4_content:
		i['fields'].insert(0, i['save'])
		
	context = {
		'query4_content' : query4_content,
		'ans' : (ans if ans else ""),
		
		'btn_class' : btn_class
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


# Add map view (optional)

test_content = [ 
	{'title': 'Topics', 'fields': [], 'disabled':'disabled', 'save': ''},
	{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Year', 'fields': [], 'disabled': 'disabled', 'save':''}
]


def test(request):
	global test_content
	global ans1 
	global ans2 
	global ans3
	global ans4
	btn_class = 'btn btn-success disabled'
	ans, query_title, query = [], "", ""
	# if ans1 == "":
		# ans1 = "temp"
	for i in test_content:
		if i['fields']: i['fields'].pop(0)

	test_content[0]['fields'], test_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")
	
	if request.method == 'POST' and request.POST.get("Topics"):
		test_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		for i in test_content[1:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		test_content[1]['fields'], test_content[1]['disabled'] = populate_form('NAME', query)
		for i in test_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Questions"):
		test_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		for i in test_content[2:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		test_content[2]['fields'], test_content[2]['disabled'] = populate_form('DATA_VALUE_TYPE', query)
		for i in test_content[3:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		test_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select year_start from chronic_disease_indicator where name = '{}' order by year_start ASC".format(ans2)
		for i in test_content[3:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		test_content[3]['fields'], test_content[3]['disabled'] = populate_form('YEAR_START', query)
		messages.success(request, query)			
		# for i in home_content[4:]:
		# 	i['disabled'] = 'disabled'

	if request.method == 'POST' and request.POST.get("Year"):
		test_content[3]['save'] = ans4 = request.POST.get("Year")

		btn_class = 'btn btn-success'

	if request.method == 'POST' and request.POST.get("submit"):
		print("here")
		# temp = ">" if query1_content[4]['save'] == "above" else "<"		
		query_title = """with temp_nat as (select * from indicator_estimate 
						where DATA_VALUE_TYPE = '{}' and year_start = {} and strat_id = 'OVR' 
						and indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')) 
						select location.name, temp_nat.data_value as location_data_value 
						from temp_nat, location 
						where temp_nat.location_id = location.location_ID""".format(ans3, ans4, ans2)
		
		with connection.cursor() as cursor:
			cursor.execute(query_title)
			ans = dictfetchall(cursor)

		messages.success(request, query_title)
		
		for i in test_content:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""

		ans1 = ans2 = ans3 = ans4 = ""
		test_content[0]['fields'], test_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")

	for i in test_content:
		i['fields'].insert(0, i['save'])

	import json
	json_test = json.dumps(ans)
	# print(json_data)


	# print(request.session.get('topic'))	
	context = {
		'test_content':test_content,
		'ans' : (ans if ans else ""),
		'ans1': (ans1 if ans1 else ""),
		'ans2': (ans2 if ans2 else ""),
		'ans3': (ans3 if ans3 else ""),
		'ans4': (ans4 if ans4 else ""), 
		'btn_class' : btn_class
		
	}

	return render(request, 'home/test.html', context)

# Advanced Search

main_content = [ 
	{'title': 'Topics', 'fields': [], 'disabled':'disabled', 'save': ''},
	{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Year', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Location', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Population', 'fields': [], 'disabled': 'disabled', 'save':''}
]

def main(request):
	global main_content
	global ans1 
	global ans2 
	global ans3
	global ans4
	global ans5
	global ans6

	ans, query_title = [], ""

	main_content[0]['fields'], main_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain order by name asc")
	main_content[1]['fields'], main_content[1]['disabled'] = populate_form('NAME', "Select distinct name from CHRONIC_DISEASE_INDICATOR order by name asc")
	main_content[2]['fields'], main_content[2]['disabled'] = populate_form('DATA_VALUE_TYPE', "Select distinct data_value_type from indicator_estimate order by data_value_type asc")
	main_content[3]['fields'], main_content[3]['disabled'] = populate_form('YEAR_START', "Select distinct year_start from CHRONIC_DISEASE_INDICATOR order by YEAR_START asc")
	main_content[4]['fields'], main_content[4]['disabled'] = populate_form('NAME', "Select distinct name from location order by name asc")
	main_content[5]['fields'], main_content[5]['disabled'] = populate_form('Population', "Select  distinct(gender || race || overall) p from populationid order by p asc")

	btn_class = 'btn btn-success'

	if request.method == 'POST' and request.POST.get("submit"):
		print("here")
		# for i in main_content['title']:
		# 	if request.POST.get(i):
		# 	 	main_content[i]['save'] = request.POST.get(i)

		temp = []
		for i in range(0, 6):
			temp.append('is not null') if main_content[i]['save'] == '' else temp.append('in {}'.format(main_content[i]))	
			
		query_title = """with all_data as 
		(select hd.NAME topic,  cdi.NAME question, ie.data_value_type indicator, cdi.YEAR_START year, ie.data_value value, ie.data_unit unit, ie.data_source source, l.name location, (p.gender || p.race || p.overall) population
		from DB4.HEALTH_DOMAIN hd, DB4.CHRONIC_DISEASE_INDICATOR cdi, DB4.INDICATOR_ESTIMATE ie,DB4.LOCATION l, DB4.POPULATIONID p
		where hd.domain_id = cdi.domain_id and cdi.indicator_id = ie.indicator_id and cdi.year_start = ie.year_start and ie.location_id = l.location_id and ie.strat_id = p.stratid and ie.data_value is not null)
		select * from all_data
		where topic {} and question {} and indicator {} and year {} and location {} and population {}
		order by topic, question, indicator, year, location, population asc
		""".format(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
		
		with connection.cursor() as cursor:
			cursor.execute(query_title)
			ans = dictfetchall(cursor)

		messages.success(request, query_title)

		ans1 = ans2 = ans3 = ans4 = ans5 = ans6 = ""
	
	context = {
		'main_content':main_content,
		'ans' : (ans if ans else ""),
		'ans1': (ans1 if ans1 else ""),
		'ans2': (ans2 if ans2 else ""),
		'ans3': (ans3 if ans3 else ""),
		'ans4': (ans4 if ans4 else ""), 
		'ans5': (ans5 if ans5 else ""), 
		'ans6': (ans6 if ans6 else ""), 
		'btn_class' : btn_class	
	}

	return render(request, 'home/main.html', context)
