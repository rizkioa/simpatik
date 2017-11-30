from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin import site
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

@login_required
def index(request):
	extra_context = {}
	extra_context.update({'has_permission': True })
	return render(request, "admin/dashboard.html",extra_context,)

@login_required
def admin_home(request):
	if not request.user.is_admin:
		return HttpResponseRedirect(reverse('useradmin:index'))
	return site.index(request)

@login_required
def user_home(request):
	if request.user.is_admin:
		return HttpResponseRedirect(reverse('admin:index'))
	return site.index(request)