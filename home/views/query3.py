query3_content = [
    {'title': 'Topics', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Year', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Population', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Highest/Lowest', 'fields': [], 'disabled': 'disabled', 'save': ''}
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
		if i['fields']:
			i['fields'].pop(0)

	query3_content[0]['fields'], query3_content[0]['disabled'] = populate_form(
		'NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("Topics"):
		query3_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(
			ans1)
		query3_content[1]['fields'], query3_content[1]['disabled'] = populate_form(
			'NAME', query)
		for i in query3_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Questions"):
		query3_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(
			ans2)
		query3_content[2]['fields'], query3_content[2]['disabled'] = populate_form(
			'DATA_VALUE_TYPE', query)
		for i in query3_content[3:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query3_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(
			ans2)
		query3_content[3]['fields'], query3_content[3]['disabled'] = populate_form(
			'YEAR_START', query)
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
		query3_content[4]['fields'], query3_content[4]['disabled'] = populate_form(
			'POPULATION', query)
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Population"):
		query3_content[4]['save'] = ans5 = request.POST.get("Population")
		query3_content[5]['fields'], query3_content[5]['disabled'] = [
			"highest", "lowest"], "btn btn-success"
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Highest/Lowest"):
		query3_content[5]['save'] = ans6 = request.POST.get("Highest/Lowest")
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

		print(ans)
		print(query_title)
		messages.success(request, query_title)
		for i in query3_content:
			i['fields'], i['disabled'], i['save'] = [], "btn btn-success disabled", ''

		query3_content[0]['fields'], query3_content[0]['disabled'] = populate_form(
			'NAME', "Select distinct name from health_domain")
		ans1 = ans2 = asn3 = ans4 = ans5 = ans6 = ""

	for i in query3_content:
		i['fields'].insert(0, i['save'])

	context = {
		'query3_content': query3_content,
		'ans': (ans if ans else ""),


		'btn_class': btn_class
	}
	return render(request, 'home/query3.html', context)
