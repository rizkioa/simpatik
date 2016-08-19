from django.template import RequestContext, loader
from django.http import HttpResponse

def add_wizard_siup(admin_, request):
	extra_context = {}

	template = loader.get_template("admin/izin/izin/form_siup.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))