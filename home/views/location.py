from .helper import *

location_content = [
    {'title': 'Topics', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save': ''},
   	{'title': 'Increase/Decrease', 'fields': [],'disabled': 'disabled', 'save': ''}
]

ans1 = ans2 = ans3 = ""
csv_data = []
def location(request):
	global location_content
	global ans1
	global ans2
	global ans3
	global csv_data
#<<<<<<< HEAD
	ans, query_title, query = [], "", ""
	btn_class = 'btn btn-success disabled'

	for i in location_content:
		if i['fields']: i['fields'].pop(0)

	ans1 == ""

	location_content[0]['fields'], location_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")
	
	if request.method == 'POST' and request.POST.get("Topics"):
		location_content[0]['save'] = ans1 = request.POST.get("Topics")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(ans1)
		location_content[1]['fields'], location_content[1]['disabled'] = populate_form('NAME', query)
		for i in location_content[2:]:
			i['disabled'] = 'disabled'

	if request.method == 'POST' and request.POST.get("Questions"):
		location_content[1]['save'] = ans2 = request.POST.get("Questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(ans2)
		location_content[2]['fields'], location_content[2]['disabled'] = populate_form('DATA_VALUE_TYPE', query)
		for i in location_content[3:]:
			i['disabled'] = 'disabled'

	if request.method == 'POST' and request.POST.get("Indicator"):
		location_content[2]['save'] = ans3 = request.POST.get("Indicator")
		query = "select distinct year_start from chronic_disease_indicator where name = '{}' and year_start >= 2007 order by year_start ASC".format(ans2)
		location_content[3]['fields'], location_content[3]['disabled'] = ["increase", "decrease"], ""
		for i in location_content[4:]:
			i['disabled'] = 'disabled'

	if request.method == 'POST' and request.POST.get("Increase/Decrease"):
		location_content[3]['save'] = request.POST.get("Increase/Decrease")
		btn_class = 'btn btn-success'
	
	if request.method == 'POST' and request.POST.get('submit'):
		topic, question, indicator = ans1, ans2, ans3
		print(location_content[3]['save'])
		temp = "asc" if location_content[3]['save'] != "increase" else "desc"
		print(temp)
		query_title = """select *
from (
  select year_1, year_2, ROUND(((yr_2_value - yr_1_value)/yr_1_value), 3) as percent_difference, location_name
  from
      (select cdi.year_start as year_1, ind_est.data_value as yr_1_value, ind_est.indicator_ID as id1,
        ind_est.location_id as location_1
      from indicator_estimate ind_est, chronic_disease_indicator cdi, health_domain dom
      where cdi.indicator_ID = ind_est.indicator_ID 
        AND cdi.year_start = ind_est.year_start 
        AND dom.domain_ID = cdi.domain_ID 
        AND dom.name = '{}'
        AND cdi.name ='{}' 
        AND ind_est.data_value_type = '{}'
        AND ind_est.strat_id = 'OVR'
        AND ind_est.data_value is not null)
      JOIN
      (select cdi.year_start as year_2, ind_est.data_value as yr_2_value, ind_est.indicator_ID as id2,
        ind_est.location_id as location_2, loc.name as location_name
      from indicator_estimate ind_est, chronic_disease_indicator cdi, 
        health_domain dom, location loc
      where cdi.indicator_ID = ind_est.indicator_ID 
        AND cdi.year_start = ind_est.year_start 
        AND dom.domain_ID = cdi.domain_ID 
        AND dom.name = '{}' 
        AND cdi.name ='{}' 
        AND ind_est.data_value_type = '{}'
        AND ind_est.strat_id = 'OVR'
        AND ind_est.data_value is not null
        AND loc.location_id = ind_est.location_id)
      on id1 = id2
    where year_1 < year_2 AND location_1 = location_2
    order by percent_difference {})
where ROWNUM < 11
				""".format(ans1, ans2, ans3, ans1, ans2, ans3, temp)
		
		with connection.cursor() as cursor:
			cursor.execute(query_title)
			ans = dictfetchall(cursor)

		for i in ans:
			i['PERCENT_DIFFERENCE'] = str(abs(i['PERCENT_DIFFERENCE']))
			
		csv_data = ans

		location_content[0]['fields'], location_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain")
		
	if request.method == 'POST' and request.POST.get('export'):
		return export_csv_file(request, csv_data)


	json_data = json.dumps(ans)


		
	
	for i in location_content:
		if i['fields']: i['fields'].insert(0, i['save'])

	context = {
		'location_content' : location_content,
		'ans' : (ans if ans else ""),
		'query_title' : query_title,
		'query' : query,
		'btn_class' : btn_class,
		'json_data': json_data
	}
	return render(request, 'home/location.html', context)
