from .helper import *

main_content = [ 
    {'title': 'Topics', 'fields': [], 'disabled':'disabled', 'save': ''},
    {'title': 'Questions', 'fields': [], 'disabled': 'disabled', 'save':''},
    {'title': 'Indicator', 'fields': [], 'disabled': 'disabled', 'save':''},
    {'title': 'Year', 'fields': [], 'disabled': '', 'save':''},
    {'title': 'Location', 'fields': [], 'disabled': '', 'save':''},
    {'title': 'Population', 'fields': [], 'disabled': '', 'save':''}
]

ans1 = ans2 = ans3 = ans4 = ans5 = ans6 = ""

def index(request):
    global main_content
    global ans1 
    global ans2 
    global ans3
    global ans4
    global ans5
    global ans6
    global csv_data

    ans, query_title = [], ""

    total = ""
    
    if request.method == 'POST' and request.POST.get('submit'):
        query = '''with temp_count as
        ((select count(rowid)as number_of_rows from CHRONIC_DISEASE_INDICATOR) union
        (select count(rowid) as number_of_rows from INDICATOR_ESTIMATE) union
        (select count(rowid) as number_of_rows from POPULATIONID) union
        (select count(rowid) as number_of_rows from HEALTH_DOMAIN) union
        (select count(rowid) as number_of_rows from location))
        select sum(number_of_rows) as total_no_of_tuples from temp_count
        '''
        with connection.cursor() as cursor:
            cursor.execute(query)
            total = dictfetchall(cursor)[0]['TOTAL_NO_OF_TUPLES']

        messages.success(request, query)

    main_content[0]['fields'], main_content[0]['disabled'] = populate_form('NAME', "Select distinct name from health_domain order by name asc")
    main_content[1]['fields'], main_content[1]['disabled'] = populate_form('NAME', "Select distinct name from CHRONIC_DISEASE_INDICATOR order by name asc")
    main_content[2]['fields'], main_content[2]['disabled'] = populate_form('DATA_VALUE_TYPE', "Select distinct data_value_type from indicator_estimate order by data_value_type asc")
    main_content[3]['fields'], main_content[3]['disabled'] = populate_form('YEAR_START', "Select distinct year_start from CHRONIC_DISEASE_INDICATOR order by YEAR_START asc")
    main_content[4]['fields'], main_content[4]['disabled'] = populate_form('NAME', "Select distinct name from location order by name asc")
    main_content[5]['fields'], main_content[5]['disabled'] = populate_form('POPULATION', "Select  distinct(gender || race || overall) population from populationid order by population asc")

    if request.method == 'POST' and request.POST.get("Topics"):
        main_content[0]['save']  = ans1 = list_to_query(request.POST.getlist('choices[]'))
        query = "select distinct cdi.name from chronic_disease_indicator cdi, health_domain hd where cdi.domain_id = hd.domain_id and hd.name {}  order by cdi.name asc".format(temp_fill(ans1))
        query2 = "select distinct cdi.year_start from chronic_disease_indicator cdi, health_domain hd where cdi.domain_id = hd.domain_id and hd.name {}  order by cdi.year_start asc".format(temp_fill(ans1))
        for i in main_content[1:3]:
            i['fields'], i['disabled'], i['save'] = [], "disabled", ""
        main_content[1]['fields'], main_content[1]['disabled'] = populate_form('NAME', query)
        main_content[3]['fields'], main_content[3]['disabled'] = populate_form('YEAR_START', query2)
        messages.success(request, query)
        messages.success(request, query2)

    if request.method == 'POST' and request.POST.get("Questions"):
        main_content[1]['save']  = ans2 = list_to_query(request.POST.getlist('choices[]'))
        query = "Select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name {}) order by data_value_type asc".format(temp_fill(ans2))
        query2 = "select distinct year_start from chronic_disease_indicator where name {} order by year_start ASC".format(temp_fill(ans2))        
        for i in main_content[2:3]:
            i['fields'], i['disabled'], i['save'] = [], "disabled", ""
        main_content[2]['fields'], main_content[2]['disabled'] = populate_form('DATA_VALUE_TYPE', query)
        main_content[3]['fields'], main_content[3]['disabled'] = populate_form('YEAR_START', query2)
        messages.success(request, query)
        messages.success(request, query2)


    if request.method == 'POST' and request.POST.get("Indicator"):
        main_content[2]['save']  = ans3 = list_to_query(request.POST.getlist('choices[]'))
        query = "select distinct year_start from chronic_disease_indicator where name {} order by year_start ASC".format(temp_fill(ans2))
        main_content[3]['fields'], main_content[3]['disabled'] = populate_form('YEAR_START', query)
        messages.success(request, query)

    if request.method == 'POST' and request.POST.get("Year"):
        main_content[3]['save']  = ans4 = list_to_query(request.POST.getlist('choices[]'))

    if request.method == 'POST' and request.POST.get("Location"):
        main_content[4]['save']  = ans5 = list_to_query(request.POST.getlist('choices[]'))

    if request.method == 'POST' and request.POST.get("Population"):
        main_content[5]['save']  = ans6 = list_to_query(request.POST.getlist('choices[]'))

    btn_class = 'btn btn-success'

    if request.method == 'POST' and request.POST.get("search"):            
        query_title = """with all_data as 
        (select hd.NAME topic,  cdi.NAME question, ie.data_value_type indicator, cdi.YEAR_START year, ie.data_value value, ie.data_unit unit, ie.data_source source, l.name location, (p.gender || p.race || p.overall) population
        from HEALTH_DOMAIN hd, CHRONIC_DISEASE_INDICATOR cdi, INDICATOR_ESTIMATE ie,LOCATION l, POPULATIONID p
        where hd.domain_id = cdi.domain_id and cdi.indicator_id = ie.indicator_id and cdi.year_start = ie.year_start and ie.location_id = l.location_id and ie.strat_id = p.stratid and ie.data_value is not null)
        select * from all_data
        where topic {} and question {} and indicator {} and year {} and location {} and population {}
        order by topic, question, indicator, year, location, population asc
        """.format(temp_fill(ans1), temp_fill(ans2), temp_fill(ans3), temp_fill(ans4), temp_fill(ans5), temp_fill(ans6))
        
        with connection.cursor() as cursor:
            cursor.execute(query_title)
            ans = dictfetchall(cursor)
        
        csv_data = ans
        
        messages.success(request, query_title)
        
    if request.method == 'POST' and request.POST.get('export'):
        return export_csv_file(request, csv_data)

    if request.POST.get('refresh'):
        for i in main_content:
            i['fields'], i['disabled'], i['save'] = [], "disabled", ''
        ans = ans1 = ans2 = ans3 = ans4 = ans5 = ans6 = temp1 = temp2 = temp3 = temp4 = temp5 = temp6 = ""

        main_content[0]['fields'], main_content[0]['disabled'] = populate_form(
			'NAME', "Select distinct name from health_domain order by name")

    context = {
        'total': total,
        'main_content': main_content,
        'ans' : (ans if ans else ""),
        'ans1': (ans1 if ans1 else ""),
        'ans2': (ans2 if ans2 else ""),
        'ans3': (ans3 if ans3 else ""),
        'ans4': (ans4 if ans4 else ""), 
        'ans5': (ans5 if ans5 else ""), 
        'ans6': (ans6 if ans6 else ""), 
        'btn_class' : btn_class
    }
    
    return render(request, 'home/index.html', context)


