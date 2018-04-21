from django.shortcuts import render

query1_content = [
	{'title': 'Topics', 'fields': [], 'disabled':'disabled', 'save': ''},
	{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Year', 'fields': [], 'disabled': 'disabled', 'save':''},
	{'title': 'Above/Below', 'fields': [], 'disabled': 'disabled', 'save':''}
]
ans1 = ans2 = ans3 = ans4 = ans5 = ""

def query1(request):
	global query1_content
	global ans1
	global ans2
	global ans3
	global ans4
	global ans5
	btn_class = 'btn btn-success disabled'
	ans, query_title, query = [], "", ""
	national_avg = ""
	# if ans1 == "":
	# ans1 = "temp"
	for i in query1_content:
		if i['fields']:
			i['fields'].pop(0)

	query1_content[0]['fields'], query1_content[0]['disabled'] = populate_form(
		'NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("Topics"):
		query1_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(
			ans1)
		for i in query1_content[1:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		query1_content[1]['fields'], query1_content[1]['disabled'] = populate_form(
			'NAME', query)
		for i in query1_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Questions"):
		query1_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(
			ans2)
		for i in query1_content[2:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		query1_content[2]['fields'], query1_content[2]['disabled'] = populate_form(
			'DATA_VALUE_TYPE', query)
		for i in query1_content[3:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		query1_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select year_start from chronic_disease_indicator where name = '{}' order by year_start ASC".format(
			ans2)
		for i in query1_content[3:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		query1_content[3]['fields'], query1_content[3]['disabled'] = populate_form(
			'YEAR_START', query)
		messages.success(request, query)

		for i in query1_content[4:]:
			i['disabled'] = 'disabled'

	if request.method == 'POST' and request.POST.get("Year"):
		query1_content[3]['save'] = ans4 = request.POST.get("Year")

		for i in query1_content[4:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""

		query1_content[4]['fields'], query1_content[4]['disabled'] = [
			'above', 'below'], ''

		for i in query1_content[5:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Above/Below"):
		query1_content[4]['save'] = ans5 = request.POST.get("Above/Below")
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
								temp_nat.data_value as location_data_value from temp_nat, location 
									where temp_nat.location_id = location.location_ID and temp_nat.data_value {} (select avg(data_value) from temp_nat)
				""".format(ans3, ans4, ans2, temp)

		with connection.cursor() as cursor:
			cursor.execute(query_title)
			ans = dictfetchall(cursor)

		messages.success(request, query_title)
		national_avg = ans[0]['NATIONAL_AVG']

		for i in query1_content:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""

		# ans1 = ans2 = ans3 = ans4 = ans5 = ""
		query1_content[0]['fields'], query1_content[0]['disabled'] = populate_form(
			'NAME', "Select distinct name from health_domain")

	for i in query1_content:
		i['fields'].insert(0, i['save'])

	import json
	json_data = json.dumps(ans)
	# print(json_data)

	# print(request.session.get('topic'))
	context = {
		'query1_content': query1_content,
		'ans': (ans if ans else ""),
		'ans1': (ans1 if ans1 else ""),
		'ans2': (ans2 if ans2 else ""),
		'ans3': (ans3 if ans3 else ""),
		'ans4': (ans4 if ans4 else ""),
		'ans5': (ans5 if ans5 else ""),
		'json_data': json_data,
		'btn_class': btn_class,
		'national_avg': national_avg

	}
	return render(request, 'home/query1.html', context)
