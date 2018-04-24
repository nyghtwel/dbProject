from .helper import *
import re

indicators_content = [
    {'title': 'Topics', 'fields': [], 'disabled': 'disabled', 'save': ''},
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

		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where domain_id in (select domain_id from health_domain where name = '{}'))".format(ans1)
		for i in indicators_content[1:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		indicators_content[1]['fields'], indicators_content[1]['disabled'] = populate_form(
			'DATA_VALUE_TYPE', query)
		for i in indicators_content[2:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)


	if request.method == 'POST' and request.POST.get("Indicator"):
		indicators_content[1]['save'] = ans2 = request.POST.get("Indicator")
		query = "select distinct year_start from indicator_estimate where data_value_type = '{}' and year_start >= 2007 and indicator_id in (select indicator_id from chronic_disease_indicator where domain_id in (select domain_id from health_domain where name = '{}')) order by year_start ASC".format(
			ans2, ans1)
		for i in indicators_content[2:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		indicators_content[2]['fields'], indicators_content[2]['disabled'] = populate_form(
			'YEAR_START', query)
		for i in indicators_content[3:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year Start"):
		indicators_content[2]['save'] = ans3 = request.POST.get("Year Start")
		query = "select distinct year_end from chronic_disease_indicator where year_end > {} and indicator_id in (select indicator_id from chronic_disease_indicator where domain_id in (select domain_id from health_domain where name = '{}')) order by year_end ASC".format(
			ans3, ans1)
		for i in indicators_content[3:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		indicators_content[3]['fields'], indicators_content[3]['disabled'] = populate_form(
			'YEAR_END', query)
		for i in indicators_content[4:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Year End"):
		indicators_content[3]['save'] = ans4 = request.POST.get("Year End")
		for i in indicators_content[4:]:
			i['fields'], i['disabled'], i['save'] = [], "disabled", ""
		indicators_content[4]['fields'], indicators_content[4]['disabled'] = [
			"increase", "decrease"], ""
		for i in indicators_content[5:]:
			i['disabled'] = 'disabled'
		messages.success(request, query)

	if request.method == 'POST' and request.POST.get("Increase/Decrease"):
		indicators_content[4]['save'] = request.POST.get("Increase/Decrease")
		btn_class = 'btn btn-success'

	" Column names for table "
	avg_val_year_1 = 'AVG_VAL_' + str(ans3)
	avg_val_year_2 = 'AVG_VAL_' + str(ans4)

	" Title for table and graph "
	title_temp = indicators_content[4]['save'] + 'd'
	title = 'Indicators for {} that {} in {} from {} to {}'.format(ans1, title_temp.capitalize(), ans2, ans3, ans4)

	if request.method == 'POST' and request.POST.get('submit'):
		topic, indicator, y1, y2 = ans1, ans2, ans3, ans4
		temp = "<" if indicators_content[4]['save'] == "decrease" else ">"
		query_title = """
			select id1 as question, round(dat_val1 , 3) as avg_val_{}, round(dat_val2 , 3) as avg_val_{} from (
					select hd.name as name1,
					cdi.name as id1, 
					ie.DATA_VALUE_TYPE as type1,
					avg(ie.data_value) as dat_val1
					from indicator_estimate ie, chronic_disease_indicator cdi, health_domain hd where 
					ie.indicator_id = cdi.indicator_id and
					hd.domain_id = cdi.domain_id and 
					hd.name = '{}' and
					ie.year_start = '{}' and
					data_value_type = '{}' and
					data_value is not null and
					strat_id = 'OVR'
					group by hd.name, cdi.name, ie.DATA_VALUE_TYPE
					),
					(select hd.name as name2,
					cdi.name as id2, 
					ie.DATA_VALUE_TYPE as type2,
					avg(ie.data_value) as dat_val2
					from indicator_estimate ie, chronic_disease_indicator cdi, health_domain hd where 
					ie.indicator_id = cdi.indicator_id and
					hd.domain_id = cdi.domain_id and 
					hd.name = '{}' and
					ie.year_start = '{}' and
					data_value_type = '{}' and
					data_value is not null and
					strat_id = 'OVR'
					group by hd.name, cdi.name, ie.DATA_VALUE_TYPE)
					
			where  name1 = name2 and
			id1 = id2 and
			type1 = type2 and
			dat_val2 {} dat_val1
			""".format(y1, y2, topic, y1, indicator, topic, y2, indicator, temp)

		with connection.cursor() as cursor:
			cursor.execute(query_title)
			ans = dictfetchall(cursor)
			print(ans)

		# for i in indicators_content:
		# 	i['fields'], i['disabled'], i['save'] = [], "disabled", ''

		messages.success(request, query_title)

		indicators_content[0]['fields'], indicators_content[0]['disabled'] = populate_form(
			'NAME', "Select distinct name from health_domain")
		# ans1 = ans2 = asn3 = ans4 = ""

	for i in indicators_content:
		i['fields'].insert(0, i['save'])


	for i in ans:
		temp_avg1 = i[avg_val_year_1]
		temp_avg2 = i[avg_val_year_2]
		i[avg_val_year_1] = str(temp_avg1)
		i[avg_val_year_2] = str(temp_avg2)


	print(ans)
	json_data = json.dumps(ans)
	json_title = json.dumps(title)
	context = {
		'indicators_content': indicators_content,
		'ans': (ans if ans else ""),
		'btn_class': btn_class,
		'json_data': json_data,
		'title': json_title
	}
	return render(request, 'home/indicators.html', context)
