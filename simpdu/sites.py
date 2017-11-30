from django.contrib import admin
from django.http import HttpResponseRedirect, QueryDict
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.core.urlresolvers import reverse

def _redirect_url(request):
	if request.user.is_authenticated():
		if request.user.is_admin:
			next = '/admin/'
		else:
			next = '/user/'
	else:
		next = request.GET.get(REDIRECT_FIELD_NAME)
		if next:
			next = next.split("next=")[-1]
		else:
			next = '/user/'
	return next

class UserAdminSite(admin.AdminSite):

	def has_permission(self, request):

		return request.user.is_active and not request.user.is_admin
	
	@never_cache
	def login(self, request, extra_context=None):
		next_page = _redirect_url(request)
		if request.method == 'GET' and self.has_permission(request):
			index_path = reverse('useradmin:index', current_app=self.name)
			return HttpResponseRedirect(index_path)
		elif request.user.is_authenticated():
			return HttpResponseRedirect(next_page)
		
		if request.method == 'POST':
			form = AuthenticationForm(request, data=request.POST)
			username = request.POST.get('username', None)
			password = request.POST.get('password', None)
			user = authenticate(username=username, password=password)
			
			if user is not None:
				if user.is_admin:
					admin.site.login(request, extra_context)
					return HttpResponseRedirect('/admin/')
				else:
					return HttpResponseRedirect('/user/')
			else:
				return HttpResponseRedirect('/user/login/')
		else:
			form = AuthenticationForm(request)

		current_site = get_current_site(request)
		context = {
			'form': form,
			REDIRECT_FIELD_NAME: next_page,
			'site': current_site,
			'site_name': current_site.name,
		}
		if extra_context is not None:
			context.update(extra_context)

		# if current_app is not None:
		# 	request.current_app = current_app
		template_name='admin/login.html'
		return TemplateResponse(request, template_name, context)
		
usersite = UserAdminSite(name='useradmin')