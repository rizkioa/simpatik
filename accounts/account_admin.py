from accounts.forms import AccountChangeForm
from accounts.models import Account
from accounts.utils import save_sync_siabjo

from django.contrib import admin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.shortcuts import render
from simpdu.sites import usersite

from master.utils import get_param
from master.models import Negara

import drest

class AccountAdmin(UserAdmin):
	form = AccountChangeForm
	list_display = ('username', 'nama_lengkap', 'is_admin', 'login_as')
	list_filter = ('is_admin', 'status', 'is_active')
	search_fields = ('username', 'nama_lengkap', 'alamat', 'telephone', 'email', 'tempat_lahir',)
	ordering = ('id',)
	readonly_fields = ('last_login', 'created_at', 'updated_at')
	filter_horizontal = ()

	fieldsets = (
		(None, {'fields': ('nama_lengkap', 'username', 'password')}),
		('Personal info', {'fields': ('tempat_lahir', 'tanggal_lahir','telephone', 'email', 'kewarganegaraan','foto',)}),
		('Alamat', {'fields': ('alamat', 'negara', 'provinsi', 'kabupaten', 'kecamatan', 'desa', ('lintang','bujur'))}),
		('Hak Akses', {'fields': ('groups', 'user_permissions', 'status', 'is_active','is_admin','is_superuser','last_login', 'created_at', 'updated_at')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('nama_lengkap', 'username', 'password1', 'password2')}
		),
	)

	def login_as(self, obj):
		return mark_safe('<a class="btn btn-xs btn-info" title="Login sebagai %s" href="%s"><i style="margin: 0px;" class="fa fa-eye"></i></a>' % (obj.nama_lengkap,reverse('loginas-user-login', kwargs={'user_id': obj.id })))
	login_as.short_description = 'Login Sebagai'

	def get_readonly_fields(self, request, obj=None):
		rf = ('last_login', 'created_at', 'updated_at')
		return rf

	@method_decorator(user_passes_test(lambda u: u.is_authenticated()))
	def sync_siabjo(self, request, username, extra_context=None):
		if not request.user.is_superuser and not request.user.groups.filter(name='Admin Sistem').exists():
			if request.user.username != username:
				self.message_user(request, 'Anda tidak dapat melakukan proses ini.')
				return HttpResponseRedirect('/admin/')
		user = Account.objects.filter(username=username)
		if user.exists():
			user = user.last()
			extra_context = {}
			api_url = get_param('api_url')
			api_user_name = get_param('api_user_name')
			api_key = get_param('api_key')
			pesan = None
			foto = '/static/images/no-avatar.jpg'

			if api_url and api_user_name and api_key:
				api = drest.api.TastyPieAPI(api_url.value)
				api.auth(api_user_name.value, api_key.value)
				get_params = dict(nomor_identitas = username, limit=0,)
				data = api.pegawai.get(params=get_params)
				if data.status == 200 :
					try :
						obj_data = data.data['objects']
						if len(obj_data) > 0:
							data_profil = obj_data[0]
							if data_profil['foto'] and data_profil['foto'] != '':
								foto = data_profil['foto']
							if request.method == 'POST':
								siabjo = save_sync_siabjo(user, data_profil)
								if siabjo:
									self.message_user(request, 'Sinkronisasi Data Siabjo Selesai.')
									return HttpResponseRedirect(reverse('lihat_profile', kwargs={'username': username}))
							extra_context.update({'data': data_profil})
						else:
							pesan = '[X200]. Data tidak ditemukan.'
					except KeyError :
						pesan = '[X200]. Sinkronisasi gagal, data yg diterima tidak sesuai.'
				else:
					pesan = '[X200]. Koneksi server error, coba beberapa saat kemudian.'
				foto = api_url.value.split("/api/")[0]+foto
			else:
				pesan = 'Belum ada settingan untuk Web Service.'

			extra_context.update({'foto': foto})
		else:
			self.message_user(request, 'Nama pengguna tidak ditemukan.')
			return HttpResponseRedirect('/')
		if pesan:
			self.message_user(request, pesan)
		template = loader.get_template('admin/accounts/account/sync_siabjo_confirmation.html')
		extra_context = RequestContext(request, extra_context)
		return HttpResponse(template.render(extra_context))

	@method_decorator(user_passes_test(lambda u: u.is_authenticated()))
	def ganti_password(self, request, extra_context=None):
		from django.contrib.admin.forms import AdminPasswordChangeForm
		from django.contrib.auth.views import password_change
		
		# if request.user.is_admin:
		url = reverse('admin:password_change_done', current_app=admin.site.name)
		defaults = {
			'current_app': admin.site.name,
			'post_change_redirect': url,
			'extra_context': dict(admin.site.each_context(request), **(extra_context or {})),
		}
		defaults['password_change_form'] = AdminPasswordChangeForm
		if admin.site.password_change_template is not None:
			defaults['template_name'] = admin.site.password_change_template
		return password_change(request, **defaults)
		# else:
		# 	post_change_redirect = reverse('admin:password_change_done', current_app=usersite.name)
		# 	from accounts.forms import CustomPasswordChangeForm
		# 	if request.method == "POST":
		# 		form = CustomPasswordChangeForm(user=request.user, data=request.POST)
		# 		if form.is_valid():
		# 			form.save()
		# 			update_session_auth_hash(request, form.user)
		# 			return HttpResponseRedirect(post_change_redirect)
		# 	else:
		# 		form = CustomPasswordChangeForm(user=request.user)
		# 	context = {
		# 		'form': form,
		# 		'title': ('Password change'),
		# 	}
		# 	context.update(dict(usersite.each_context(request), **(extra_context or {})))
		# 	request.current_app = usersite.name
		# 	if admin.site.password_change_template is not None:
		# 		return TemplateResponse(request, usersite.password_change_template, context)
		# 	else:
		# 		return TemplateResponse(request, "registration/password_change_form.html", context)

	def get_form(self, request, obj=None, **kwargs):
		form = super(AccountAdmin, self).get_form(request, obj, **kwargs)
		form.request = request
		return form
	
	def get_queryset(self, request):
		qs = super(AccountAdmin, self).get_queryset(request)
		# exclude pegawai
		qs = qs.filter(pegawai__isnull=True)
		# exclude pemohon
		qs = qs.filter(pemohon__isnull=True)
		return qs

	def profile_account(self, request, extra_context={}):
		negara_list = Negara.objects.all()
		extra_context.update({
			'has_permission': True,
			'title': 'Profile',
			'negara': negara_list,
		 })
		return render(request, "admin/accounts/account/profile.html", extra_context)

	def get_urls(self):
		from django.conf.urls import patterns, url
		
		urls = super(AccountAdmin, self).get_urls()
		my_urls = patterns('',
				url(r'^profile/$', self.profile_account, name='profile_account'),
				url(r'^password_change/$', self.ganti_password, name='password_change'),
				url(r'^sync_siabjo/(?P<username>\w+)/$', self.sync_siabjo, name='sync_siabjo'),
		)
		return my_urls + urls

	def suit_cell_attributes(self, obj, column):
		if column in ['is_admin', 'login_as']:
			return {'class': 'text-center'}
		else:
			return None