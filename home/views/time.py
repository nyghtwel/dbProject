from .helper import *

time_content = [
    {'title': 'Topics', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Year_Start', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Year_End', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Increase/Decrease', 'fields': [], 'disabled': 'disabled', 'save': ''}
]

ans1 = ans2 = ans3 = ans4 = ans5 = ""
def time(request):
	global time_content
	global ans1
	global ans2
	global ans3
	global ans4
	global ans5
	btn_class = 'btn btn-success disabled'

	for i in time_content:
		if i['fields']:
			i['fields'].pop(0)

	ans, query_title, query = [], "", ""
	ans1 == ""
	time_content[0]['fields'], time_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")

	'''
	pattern:
		1) clear fields, clear save, and set to disable 
		2) populate form from query
		3) disable the form after the next one
	'''
	if request.method == 'POST' and request.POST.get("Topics"):
		time_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		
		# clear prev fields before populating
		for i in time_content[1:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""

		time_content[1]['fields'], time_content[1]['disabled'] = populate_form('NAME', query)
		for i in time_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Questions"):
		time_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		for i in time_content[2:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		time_content[2]['fields'], time_content[2]['disabled'] = populate_form('DATA_VALUE_TYPE', query)
		for i in time_content[3:]:
			i['disabled'] = 'disabled'

		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		time_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(ans2)
		for i in time_content[3:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		time_content[3]['fields'], time_content[3]['disabled'] = populate_form('YEAR_START', query)
		for i in time_content[4:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year_Start"):
		time_content[3]['save'] = ans4 = request.POST.get("Year_Start")
		query = "select distinct year_end from chronic_disease_indicator where name = '{}' and year_end > {} order by year_end ASC".format(ans2, ans4)
		for i in time_content[4:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		time_content[4]['fields'], time_content[4]['disabled'] = populate_form('YEAR_END', query)
		for i in time_content[5:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year_End"):
		time_content[4]['save'] = ans5 = request.POST.get("Year_End")
		for i in time_content[5:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		time_content[5]['fields'], time_content[5]['disabled'] = ['increase', 'decrease'], ''
		for i in time_content[6:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Increase/Decrease"):
		time_content[5]['save'] = ans6 = request.POST.get("Increase/Decrease")
		btn_class = 'btn btn-success'

	" Title for table and graph "
	title_temp = ''
	if time_content[5]['save'] == 'increase' : title_temp = 'an Increase'
	if time_content[5]['save'] == 'decrease' : title_temp = 'a Decrease'
	title = 'States with {} in {} from {} to {} for {}'.format(title_temp, ans3, ans4, ans5, ans2)

	if request.method == 'POST' and request.POST.get("submit"):
		temp = "<" if time_content[5]['save'] == "increase" else ">"
		query_title = """With temp_nat as (select * from indicator_estimate 
					where DATA_VALUE_TYPE= '{}'
    		            and strat_id='OVR'
						and indicator_id in (select indicator_id from CHRONIC_DISEASE_INDICATOR
							where name='{}'))
							select l.name, t1.year_start as first_year, t1.data_value as first_value,
    				   			t2.year_start as second_year, t2.data_value as second_value
								from temp_nat t1,  temp_nat t2, location l
									where t1.location_id = l.location_ID
										and t2.location_id = t1.location_id
    						  			and t1.year_start = {}
    						  			and t2.year_start = {}
    						  			and t1.data_value {} t2.data_value
				""".format(ans3, ans2, ans4, ans5, temp)

		with connection.cursor() as cursor:
			cursor.execute(query_title)
			ans = dictfetchall(cursor)
		messages.success(request, query_title)

		time_content[0]['fields'], time_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")

	json_data = json.dumps(ans)
	json_title = json.dumps(title)

	for i in time_content:
		if i['fields']: i['fields'].insert(0, i['save'])

	context = {
		'time_content': time_content,
		'ans': (ans if ans else ""),
		'btn_class': btn_class,
		'json_data': json_data,
		'title' : json_title
	}
	return render(request, 'home/time.html', context)
