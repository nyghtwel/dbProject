from .helper import *

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

	messages.success(request, query)
	context = {
		'total': total
	}
	return render(request, 'home/index.html', context)

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
        #   if request.POST.get(i):
        #       main_content[i]['save'] = request.POST.get(i)

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

