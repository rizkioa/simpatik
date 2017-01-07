from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.safestring import mark_safe

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon
from izin.models import PengajuanIzin, JenisPermohonanIzin, KelompokJenisIzin, Pemohon, DetilSIUP
from izin.izin_forms import PengajuanBaruForm, PemohonForm
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, JenisLegalitas
from django.db.models import Q

try:
	from django.utils.encoding import force_text
except ImportError:
	from django.utils.encoding import force_unicode as force_text

from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

import datetime

from izin.utils import JENIS_IZIN, formatrupiah

def add_wizard_siup(request):
	extra_context = {}
	extra_context.update({'title': 'Pengajuan Baru'})
	extra_context.update({'has_permission': True})

	if request.method == 'POST':
		if request.POST.get('nama_izin') :
			# print "POST"

			# if request.POST.get('nama_izin') and request.POST.get('kelompok_izin'):
			# 	print "if"
			# 	id_kelompok_ = request.POST.get('kelompok_izin')
			# 	id_kelompok_ = int(id_kelompok_)
				
			# 	url_ = "#"
			# 	response = HttpResponseRedirect(url_)
				# response.delete_cookie('id_kelompok_izin')
				# response.set_cookie(key='id_kelompok_izin', value=id_kelompok_)
			# else:
			kode_izin_ = request.POST.get('nama_izin') # Get name 'nama_izin' in request.POST
			# print(kode_izin_)
			try:
				id_kelompok_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=kode_izin_)
				if len(id_kelompok_list) > 1:
					id_kelompok_ = request.POST.get('kelompok_izin')
					id_kelompok_list = KelompokJenisIzin.objects.filter(id=id_kelompok_).last()
				else:
					id_kelompok_list = id_kelompok_list.last()
					id_kelompok_ = id_kelompok_list.id
				# print id_kelompok_list
				# print id_kelompok_
			except AttributeError:
				msg_ = "Kode Izin tidak diketahui. Silahkan setting kode izin di <a href='%s'> Link ini</a>" % reverse('admin:izin_jenisizin_changelist')
				messages.warning(request, msg_, extra_tags='safe')
				return HttpResponseRedirect(reverse('admin:add_wizard_izin'))


			if kode_izin_ == "Reklame":
				url_ = reverse('admin:izin_proses_reklame')
			elif kode_izin_ == "HO":
				url_ = reverse('admin:izin_proses_gangguan')
			elif id_kelompok_list.kode == "503.01.06/":
				url_ = reverse('admin:izin_proses_imb_reklame')
			elif id_kelompok_list.kode == "503.01.05/":
				url_ = reverse('admin:izin_proses_imb_umum')
			elif id_kelompok_list.kode == "503.01.04/":
				url_ = reverse('admin:izin_proses_imb_perumahan')
			elif id_kelompok_list.kode == "503.06.01/":
				url_ = reverse('admin:izin_proses_pemakaian_kekayaan_daerah')
			elif id_kelompok_list.kode == "503.08/":
				url_ = reverse('admin:izin_proses_siup')
			elif id_kelompok_list.kode == "IUJK":
				url_ = reverse('admin:izin_iujk')
			elif id_kelompok_list.id == 25:
				url_ = reverse('admin:izin_proses_tdp_pt')
			elif id_kelompok_list.kode == "503.07/":
				url_ = reverse('admin:izin_proses_lokasi') 
			elif id_kelompok_list.kode == "IPPT":
				url_ = reverse('admin:izin_proses_ippt_rumah')
			elif id_kelompok_list.kode == "HULLER":
				url_ = reverse('admin:izin_proses_huller')
			else:
				url_ = "#"

			response = HttpResponseRedirect(url_) # Redirect to url
			if id_kelompok_:
				response.set_cookie(key='id_kelompok_izin', value=id_kelompok_) # to set cookie in browser
			else:
				try:
					reklame_izin = KelompokJenisIzin.objects.filter(jenis_izin__kode=kode_izin_).last()
					reklame_izin_id = reklame_izin.id
				except AttributeError:
					msg_ = "Kode Izin tidak diketahui. Silahkan setting kode izin di <a href='%s'> Link ini</a>" % reverse('admin:izin_jenisizin_changelist')
					messages.warning(request, msg_, extra_tags='safe')
					return HttpResponseRedirect(reverse('admin:add_wizard_izin'))
				response.set_cookie(key='id_kelompok_izin', value=reklame_izin_id) # to set cookie in browser

			# print request.COOKIES
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
		kecamatan = Kecamatan.objects.filter(kabupaten_id=1083)
		jenis_pemohon = JenisPemohon.objects.all()
		bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
		jenis_penanaman_modal_list = JenisPenanamanModal.objects.all()
		kelembagaan_list = Kelembagaan.objects.all()
		jenis_legalitas_list = JenisLegalitas.objects.all()

		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Untuk SIUP
		extra_context.update({'negara': negara})
		extra_context.update({'kecamatan': kecamatan})
		extra_context.update({'kecamatan_perusahaan': kecamatan})
		extra_context.update({'jenis_pemohon': jenis_pemohon})
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		extra_context.update({'bentuk_kegiatan_usaha_list': bentuk_kegiatan_usaha_list})
		extra_context.update({'jenis_penanaman_modal_list': jenis_penanaman_modal_list})
		extra_context.update({'kelembagaan_list': kelembagaan_list})
		# extra_context.update({'produk_utama_list': produk_utama_list})
		extra_context.update({'jenis_legalitas_list': jenis_legalitas_list})
		extra_context.update({'has_permission': True })

		# +++++++++++++++++++ jika cookie pengajuan ada dan di refrash +++++++++++++++++
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "":
				try:
					pengajuan_ = DetilSIUP.objects.get(id=request.COOKIES['id_pengajuan'])
					alamat_ = ""
					alamat_perusahaan_ = ""
					if pengajuan_.pemohon:
						if pengajuan_.pemohon.desa:
							alamat_ = str(pengajuan_.pemohon.alamat)+", Ds. "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat_pemohon_konfirmasi': alamat_ })
						extra_context.update({ 'pemohon_konfirmasi': pengajuan_.pemohon })
						
						ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
						extra_context.update({ 'ktp': ktp_ })
						paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
						extra_context.update({ 'paspor': paspor_ })
					if pengajuan_.perusahaan:
						if pengajuan_.perusahaan.desa:
							alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Ds. "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat_perusahaan_konfirmasi': alamat_perusahaan_ })
						extra_context.update({ 'perusahaan_konfirmasi': pengajuan_.perusahaan })
						legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(~Q(jenis_legalitas__id=2)).last()
						legalitas_perubahan= pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas__id=2).last()

						extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
						extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })

					extra_context.update({ 'no_pengajuan_konfirmasi': pengajuan_.no_pengajuan })
					extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
					extra_context.update({ 'kelompok_jenis_izin_konfirmasi': pengajuan_.kelompok_jenis_izin })
					if pengajuan_.bentuk_kegiatan_usaha:
						extra_context.update({ 'bentuk_kegiatan_usaha_konfirmasi': pengajuan_.bentuk_kegiatan_usaha.kegiatan_usaha })
					if pengajuan_.jenis_penanaman_modal:
						extra_context.update({ 'status_penanaman_modal_konfirmasi': pengajuan_.jenis_penanaman_modal.jenis_penanaman_modal })
					if pengajuan_.kekayaan_bersih:
						extra_context.update({ 'kekayaan_bersih_konfirmasi': "Rp "+str(pengajuan_.kekayaan_bersih) })
					if pengajuan_.total_nilai_saham:
						extra_context.update({ 'total_nilai_saham_konfirmasi': "Rp "+str(pengajuan_.total_nilai_saham) })
					if pengajuan_.presentase_saham_nasional:
						extra_context.update({ 'presentase_saham_nasional_konfirmasi': str(pengajuan_.presentase_saham_nasional)+" %" })
					if pengajuan_.presentase_saham_asing:
						extra_context.update({ 'presentase_saham_asing_konfirmasi': str(pengajuan_.presentase_saham_asing)+" %" })
					if pengajuan_.kelembagaan:
						extra_context.update({ 'kelembagaan_konfirmasi': pengajuan_.kelembagaan.kelembagaan })
					extra_context.update({ 'pengajuan_': pengajuan_ })

					template = loader.get_template("admin/izin/izin/form_wizard_siup.html")
					ec = RequestContext(request, extra_context)
					response = HttpResponse(template.render(ec))

					if pengajuan_.pemohon:
						response.set_cookie(key='id_pemohon', value=pengajuan_.pemohon.id)
					if pengajuan_.perusahaan:
						response.set_cookie(key='id_perusahaan', value=pengajuan_.perusahaan.id)
					if pengajuan_.perusahaan:
						if legalitas_pendirian:
							response.set_cookie(key='id_legalitas', value=legalitas_pendirian.id)
						if legalitas_perubahan:
							response.set_cookie(key='id_legalitas_perubahan', value=legalitas_perubahan.id)
					if ktp_:
						response.set_cookie(key='nomor_ktp', value=ktp_)
				except ObjectDoesNotExist:
					template = loader.get_template("admin/izin/izin/form_wizard_siup.html")
					ec = RequestContext(request, extra_context)
					response = HttpResponse(template.render(ec))
					response.set_cookie(key='id_pengajuan', value='0')
		else:
			template = loader.get_template("admin/izin/izin/form_wizard_siup.html")
			ec = RequestContext(request, extra_context)
			response = HttpResponse(template.render(ec))
			response.set_cookie(key='id_pengajuan', value='0')
		return response
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))

def cetak(request, id_pengajuan_izin_):
	extra_context = {}
	extra_context.update({'title': 'Pengajuan Selesai'})
	pengajuan_ = DetilSIUP.objects.get(id=id_pengajuan_izin_)
	extra_context.update({'pemohon': pengajuan_.pemohon})
	extra_context.update({'no_pengajuan': pengajuan_.no_pengajuan})
	extra_context.update({'id_pengajuan': pengajuan_.id})
	extra_context.update({'jenis_pemohon': pengajuan_.pemohon.jenis_pemohon})
	extra_context.update({'alamat_pemohon': str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)})
	extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
	extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
	extra_context.update({'created_at': pengajuan_.created_at})
	template = loader.get_template("admin/izin/izin/cetak.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))

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