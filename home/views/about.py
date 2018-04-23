from .helper import *

def about(request):
	context = {

	}
	return render(request, 'home/about.html', context)
