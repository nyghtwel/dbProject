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
		health_domain, temp = populate_form(
			'NAME', "Select distinct name from health_domain")

	if request.method == 'POST' and request.POST.get("topics"):
		ans1 = request.POST.get("topics")
		ans2 = request.POST.get("questions")
		query = "select distinct chronic_disease_indicator.name from chronic_disease_indicator, health_domain where chronic_disease_indicator.domain_id = health_domain.domain_id and health_domain.name = '{}'".format(
			ans1)
		questions_5, question_button_5 = populate_form('NAME', query)

	if request.method == 'POST' and request.POST.get("questions"):
		ans2 = request.POST.get("questions")
		query = "select distinct data_value_type from indicator_estimate where indicator_id in (select indicator_id from chronic_disease_indicator where name = '{}')".format(
			ans2)
		indicator_5, indicator_button_5 = populate_form('DATA_VALUE_TYPE', query)

	if request.method == 'POST' and request.POST.get("final"):
		ans.extend([ans1, ans2, request.POST.get("final")])
		questions_5 = indicator_5 = increase_decrease_5 = []
		question_button_5 = indicator_button_5 = increase_decrease_button_5 = "btn btn-success disabled"
		ans1 = ans2 = ""

	context = {
		'health_domain': health_domain,
		'questions': questions_5,
		'question_button': question_button_5,
		'increase_decrease': increase_decrease_5,
		'increase_decrease_button': increase_decrease_button_5,
		'ans': (ans if ans else ""),
		'query_title': query_title,
		'indicator': indicator_5,
		'indicator_button': indicator_button_5
	}
	return render(request, 'home/query5.html', context)
