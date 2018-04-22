from .helper import *

indicators_content = [
    {'title': 'Topics', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	#{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Year Start', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Year End', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Increase/Decrease', 'fields': [], 'disabled': 'disabled', 'save': ''}
]
ans1 = ans2 = ans3 = ans4 = ""

def indicators(request):
	global indicators_content
	global ans1
	global ans2
	global ans3
	global ans4
	ans, query_title, query = [], "", ""

	btn_class = 'btn btn-success disabled'
	for i in indicators_content:
		if i['fields']:
			i['fields'].pop(0)

	ans1 == ""

	indicators_content[0]['fields'], indicators_content[0]['disabled'] = populate_form(
		'NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("Topics"):
		indicators_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from health_domain where name = '{}')".format(
			ans1)
		indicators_content[1]['fields'], indicators_content[1]['disabled'] = populate_form(
			'DATA_VALUE_TYPE', query)
		for i in indicators_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	#if request.method == 'POST' and request.POST.get("Questions"):
	#	indicators_content[1]['save'] = ans2 = request.POST.get("Questions")
	#	query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(
	#		ans2)
	#	indicators_content[2]['fields'], indicators_content[2]['disabled'] = populate_form(
	#		'DATA_VALUE_TYPE', query)
	#	for i in indicators_content[3:]:
	#		i['disabled'] = 'disabled'
	#	messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Indicator"):
		indicators_content[1]['save'] = ans2 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(
			ans2)
		indicators_content[2]['fields'], indicators_content[3]['disabled'] = populate_form(
			'YEAR_START', query)
		for i in indicators_content[3:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year Start"):
		indicators_content[3]['save'] = ans3 = request.POST.get("Year Start")
		query = "select distinct year_end from chronic_disease_indicator where year_end > {} order by year_end ASC".format(
			ans4)
		indicators_content[4]['fields'], indicators_content[4]['disabled'] = populate_form(
			'YEAR_END', query)
		for i in indicators_content[5:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year End"):
		indicators_content[4]['save'] = ans4 = request.POST.get("Year End")
		indicators_content[5]['fields'], indicators_content[5]['disabled'] = [
			"increase", "decrease"], ""
		for i in indicators_content[6:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Increase/Decrease"):
		indicators_content[5]['save'] = request.POST.get("Increase/Decrease")
		btn_class = 'btn btn-success'

	if request.method == 'POST' and request.POST.get('submit'):
		topic, indicator, y1, y2 = ans1, ans2, ans3, ans4
		temp = "<" if indicators_content[4]['save'] == "increase" else ">"
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

		for i in indicators_content:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ''

		messages.success(request, query_title)

		indicators_content[0]['fields'], indicators_content[0]['disabled'] = populate_form(
			'NAME', "Select distinct name from health_domain")
		ans1 = ans2 = asn3 = ans4 = ans5 = ""

	for i in indicators_content:
		i['fields'].insert(0, i['save'])

	context = {
		'indicators_content': indicators_content,
		'ans': (ans if ans else ""),

		'btn_class': btn_class
	}
	return render(request, 'home/indicators.html', context)
