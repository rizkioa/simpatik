from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon
from izin.models import PengajuanIzin, JenisPermohonanIzin, KelompokJenisIzin, Pemohon
from izin.izin_forms import PengajuanBaruForm, PemohonForm
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna


try:
	from django.utils.encoding import force_text
except ImportError:
	from django.utils.encoding import force_unicode as force_text

from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

import datetime

from izin.utils import JENIS_IZIN
def add_wizard_siup(request):
	extra_context = {}
	extra_context.update({'title': 'Pengajuan Baru'})

	if request.method == 'POST':
		if request.POST.get('nama_izin') :
			if request.POST.get('nama_izin') and request.POST.get('kelompok_izin'):
				id_kelompok_ = request.POST.get('kelompok_izin')
				id_kelompok_ = int(id_kelompok_)
			else:
				kode_izin_ = request.POST.get('nama_izin') # Get name 'nama_izin' in request.POST
				try:
					id_kelompok_ = KelompokJenisIzin.objects.filter(jenis_izin__kode=kode_izin_).last()
					id_kelompok_ = id_kelompok_.id
				except AttributeError:
					msg_ = "Kode Izin tidak diketahui. Silahkan setting kode izin di <a href='%s'> Link ini</a>" % reverse('admin:izin_jenisizin_changelist')
					messages.warning(request, msg_, extra_tags='safe')
					return HttpResponseRedirect(reverse('admin:add_wizard_izin'))

			url_ = reverse('admin:izin_proses_siup')
			response = HttpResponseRedirect(url_) # Redirect to url
			response.set_cookie(key='id_kelompok_izin', value=id_kelompok_) # to set cookie in browser

			print request.COOKIES
			return response
		else:
			messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')


	EMPTY_JENIS_IZIN = (('', 'Select an Option'),)+JENIS_IZIN
	extra_context.update({'jenis': EMPTY_JENIS_IZIN})

	template = loader.get_template("admin/izin/izin/form_siup.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))


def formulir_siup(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		extra_context.update({'title': 'SIUP Baru'})
		negara = Negara.objects.all()
		extra_context.update({'negara': negara})
		jenis_pemohon = JenisPemohon.objects.all()
		extra_context.update({'jenis_pemohon': jenis_pemohon})
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Untuk SIUP

		# print request.COOKIES
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		template = loader.get_template("admin/izin/izin/form_wizard_siup.html")
		# template = loader.get_template("admin/izin/izin/izin_baru_form_pemohon.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))

# def formulir_siup(request):
# 	extra_context={}
# 	extra_context.update({'title': 'SIUP Baru'})
# 	negara = Negara.objects.all()
# 	extra_context.update({'negara': negara})
# 	jenis_pemohon = JenisPemohon.objects.all()
# 	extra_context.update({'jenis_pemohon': jenis_pemohon})
# 	jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin') # Untuk SIUP

# 	# print request.COOKIES
# 	extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
# 	if request.POST:
# 		form = PemohonForm(request.POST)
# 		if form.is_valid():
# 			# Untuk Pemohon
# 			jenis_pemohon_id_ = request.POST.get('jenis_pemohon', None)
# 			# End

# 			# Untuk Identitas Pribadi
# 			kewarganegaraan_ = request.POST.get('kewarganegaraan', None)
# 			alamat_ = request.POST.get('alamat', None)
# 			desa_id_ = request.POST.get('desa', None)
# 			nama_lengkap_ = request.POST.get('nama_lengkap', None)
# 			tempat_lahir_ = request.POST.get('tempat_lahir', None)
# 			tgl_lahir_ = request.POST.get('tanggal_lahir', None)
# 			telepon_ = request.POST.get('telephone', None)
# 			email_ = request.POST.get('email', None)
# 			hp_ = request.POST.get('hp', None)
# 			# End

# 			# Untuk Nomor Identitas
# 			ktp_ = request.POST.get('ktp', None)
# 			paspor_ = request.POST.get('paspor', None)
# 			# End

# 			# Untuk Pengajuan Izin
# 			jenis_permohonan_ = request.POST.get('jenis_pengajuan', None)
# 			kelompok_jenis_izin_ = request.COOKIES['id_kelompok_izin']
# 			# End

# 			# Simpan Pemohon
# 			# print form.instance

# 			if nama_lengkap_ and jenis_pemohon_id_ and desa_id_:

# 				try:
# 				    p = Pemohon.objects.get(username=ktp_)
# 				except ObjectDoesNotExist:
# 				    p, created = Pemohon.objects.get_or_create(
# 									nama_lengkap= nama_lengkap_,
# 									# defaults={'birthday': date(1940, 10, 9)},
# 									desa_id = desa_id_,
# 									jenis_pemohon_id = jenis_pemohon_id_,
# 									verified_at=datetime.datetime.now(),
# 									username=ktp_,
# 									)

# 				p.alamat = alamat_
# 				p.telephone = telepon_
# 				p.jenis_pemohon_id = jenis_pemohon_id_
# 				p.tempat_lahir = tempat_lahir_
# 				if email_:
# 					p.email = email_
# 				p.hp = hp_
# 				p.kewarganegaraan = kewarganegaraan_
# 				p.save()

# 				if created:
# 					content_type_id = ContentType.objects.get_for_model(p).pk
# 					LogEntry.objects.log_action(
# 							user_id=request.user.pk,
# 							content_type_id=content_type_id,
# 							object_id=p.id,
# 							object_repr=force_text(p),
# 							action_flag=ADDITION,
# 							change_message="Operator menambahkan IdentitasPribadi baru dari formulir pengajuan baru.",
# 						)

# 				else:
# 					content_type_id = ContentType.objects.get_for_model(p).pk
# 					LogEntry.objects.log_action(
# 							user_id=request.user.pk,
# 							content_type_id=content_type_id,
# 							object_id=p.id,
# 							object_repr=force_text(p),
# 							action_flag=CHANGE,
# 							change_message="Operator melakukan edit IdentitasPribadi dari formulir pengajuan baru.",
# 						)


# 			# Simpan Identitas
# 			if ktp_ or paspor_ :
# 				# print "OE"
# 				if ktp_:
# 					try:
# 						i = NomorIdentitasPengguna.objects.get(nomor = ktp_)
# 					except ObjectDoesNotExist:
# 						i, created = NomorIdentitasPengguna.objects.get_or_create(
# 									nomor = ktp_,
# 									jenis_identitas_id=1,
# 									user_id=p.id,
# 									)

# 					if created:
# 						content_type_id = ContentType.objects.get_for_model(i).pk
# 						LogEntry.objects.log_action(
# 								user_id=request.user.pk,
# 								content_type_id=content_type_id,
# 								object_id=i.id,
# 								object_repr=force_text(i),
# 								action_flag=ADDITION,
# 								change_message="Operator menambahkan Nomor Identitas KTP baru dari formulir pengajuan baru.",
# 							)


# 				if paspor_:
# 					try:
# 						i = NomorIdentitasPengguna.objects.get(nomor = paspor_)
# 					except ObjectDoesNotExist:
# 						i, created = NomorIdentitasPengguna.objects.get_or_create(
# 									nomor = paspor_,
# 									jenis_identitas_id=2,
# 									user_id=p.id,
# 									)

# 				if created:
# 					content_type_id = ContentType.objects.get_for_model(i).pk
# 					LogEntry.objects.log_action(
# 							user_id=request.user.pk,
# 							content_type_id=content_type_id,
# 							object_id=i.id,
# 							object_repr=force_text(i),
# 							action_flag=ADDITION,
# 							change_message="Operator menambahkan Nomor Identitas PASPOR baru dari formulir pengajuan baru.",
# 						)

# 			# SIMPAN PENGAJUAN
# 			pengajuan = PengajuanIzin(kelompok_jenis_izin_id=request.COOKIES['id_kelompok_izin'], pemohon_id=p.id,jenis_permohonan_id=jenis_permohonan_, verified_at=datetime.datetime.now(), )
# 			pengajuan.save()

# 			LogEntry.objects.log_action(
# 					user_id=request.user.pk,
# 					content_type_id=content_type_id,
# 					object_id=pengajuan.id,
# 					object_repr=force_text(pengajuan),
# 					action_flag=ADDITION,
# 					change_message="Operator melakukan pendaftaran pengajuan baru dengan nama pemohon ."+pengajuan.pemohon,
# 				)

# 			extra_context.update({'title': 'Pengajuan Selesai'})
# 			extra_context.update({'nama_pemohon': pengajuan.pemohon})		
# 			extra_context.update({'alamat_pemohon': pengajuan.pemohon.alamat })
# 			extra_context.update({'created_at': pengajuan.created_at })
# 			extra_context.update({'id_pengajuan': pengajuan.id })

# 			template = loader.get_template("admin/izin/izin/pengajuan_baru_selesai.html")
# 			ec = RequestContext(request, extra_context)
# 			return HttpResponse(template.render(ec))
# 		else:
# 			print form.errors
# 	else:
# 		form = PemohonForm()
# 	extra_context.update({'form': form})
# 	# template = loader.get_template("admin/izin/izin/form_wizard_siup.html")
# 	template = loader.get_template("admin/izin/izin/izin_baru_form_pemohon.html")
# 	ec = RequestContext(request, extra_context)
# 	return HttpResponse(template.render(ec))
