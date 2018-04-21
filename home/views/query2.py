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
		if i['fields']:
			i['fields'].pop(0)

	ans, query_title, query = [], "", ""

	# if ans1 == "":
	ans1 == ""
	query2_content[0]['fields'], query2_content[0]['disabled'] = populate_form(
		'NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("Topics"):
		query2_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(
			ans1)
		query2_content[1]['fields'], query2_content[1]['disabled'] = populate_form(
			'NAME', query)
		for i in query2_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Questions"):
		query2_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(
			ans2)
		query2_content[2]['fields'], query2_content[2]['disabled'] = populate_form(
			'DATA_VALUE_TYPE', query)
		for i in query2_content[3:]:
			i['disabled'] = 'disabled'

		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query2_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(
			ans2)
		query2_content[3]['fields'], query2_content[3]['disabled'] = populate_form(
			'YEAR_START', query)
		for i in query2_content[4:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year_Start"):
		query2_content[3]['save'] = ans4 = request.POST.get("Year_Start")
		query = "select distinct year_end from chronic_disease_indicator where name = '{}' and year_end > {} order by year_end ASC".format(
			ans2, ans4)
		query2_content[4]['fields'], query2_content[4]['disabled'] = populate_form(
			'YEAR_END', query)
		for i in query2_content[5:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year_End"):
		query2_content[4]['save'] = ans5 = request.POST.get("Year_End")
		query2_content[5]['fields'], query2_content[5]['disabled'] = [
			'increase', 'decrease'], ''
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
		query2_content[0]['fields'], query2_content[0]['disabled'] = populate_form(
			'NAME', "Select distinct name from health_domain")

	for i in query2_content:
		if i['fields']:
			i['fields'].insert(0, i['save'])

	context = {
		'query2_content': query2_content,
		'ans': (ans if ans else ""),


		'btn_class': btn_class
	}
	return render(request, 'home/query2.html', context)
