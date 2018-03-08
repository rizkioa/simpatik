from django.http import HttpResponse

from django.core.mail import EmailMessage
from django.template import Context, Template
from django.template.loader import render_to_string

from django.db.models import Q
from django.conf import settings
import datetime
import base64
import time
import json
import os

from izin.models import PengajuanIzin, DetilIMB, DetilPembayaran, SKIzin, Riwayat
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import DetilPembayaranForm
from izin.utils import send_email_html, terbilang

def detil_pembayaran_save(request):
	if request.POST:
		pengajuan_izin_id = request.POST.get('pengajuan_izin', None)
		jumlah_pembayaran_depan = request.POST.get('jumlah_pembayaran_depan')
		# jumlah_pembayaran_belakang = request.POST.get('jumlah_pembayaran_belakang', "00")
		jumlah_pembayaran = jumlah_pembayaran_depan
		try:
			detilpembayaran_obj = DetilPembayaran.objects.filter(pengajuan_izin__id=pengajuan_izin_id).last()
			sk_izin_ = SKIzin.objects.get(pengajuan_izin__id=pengajuan_izin_id)
			pembayaran = DetilPembayaranForm(request.POST, instance=detilpembayaran_obj)
		except ObjectDoesNotExist:
			pembayaran = DetilPembayaranForm(request.POST)
		if pembayaran.is_valid():
			if request.user.groups.filter(name='Kasir'):
				p = pembayaran.save(commit=False)
				p.kode = request.POST.get('kode')
				p.peruntukan = request.POST.get('peruntukan')
				p.pengajuan_izin_id = pengajuan_izin_id
				p.jumlah_pembayaran = jumlah_pembayaran
				p.tanggal_dibuat = datetime.date.today()
				p.bank_pembayaran_id = request.POST.get('bank_pembayaran')
				p.save()
				sk_izin_.status = 9
				sk_izin_.save()
				pengajuan_obj = p.pengajuan_izin
				pengajuan_obj.status = 2
				pengajuan_obj.save()
				riwayat_ = Riwayat(
					pengajuan_izin_id = p.pengajuan_izin.id,
					created_by_id = request.user.id,
					keterangan = "Kasir Verified"
				)
				riwayat_.save()
				######## start send email to pemohon ##########
				if pengajuan_obj.pemohon:
					if pengajuan_obj.pemohon.email and pengajuan_obj.pemohon.email is not None:
						# send_email_html(pengajuan_obj.pemohon.email, p.peruntukan, p, 'cetak/notifikasi_send_email.html')

						terbilang_jumlah = ""
						if p.jumlah_pembayaran:
							terbilang_jumlah = terbilang(int(p.jumlah_pembayaran.split(",")[0].replace(".", "")))

						html_content = render_to_string('cetak/notifikasi_send_email.html', {
							'obj': p,
							'total_bayar': int(p.jumlah_pembayaran.replace(".", "")),
							'terbilang_jumlah': terbilang_jumlah,
							})
						
						# email = EmailMessage(p.peruntukan, html_content, settings.DEFAULT_FROM_EMAIL, pengajuan_obj.pemohon.email)
						email = EmailMessage(p.peruntukan, html_content, settings.DEFAULT_FROM_EMAIL, [pengajuan_obj.pemohon.email])
						email.content_subtype = "html"
						res = email.send()
				######## end send email to pemohon ##########

				data = {'success': True,
						'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
						'data': {}}
				response = HttpResponse(json.dumps(data))
			# elif request.user.groups.filter(name='Operator') or request.user.is_superuser:
			# 		p = pembayaran.save(commit=False)
			# 		p.save()
			# 		p.pengajuan_izin.status = 4
			# 		p.pengajuan_izin.save()
			# 		riwayat_ = Riwayat(
			# 			pengajuan_izin_id = p.pengajuan_izin.id,
			# 			created_by_id = request.user.id,
			# 			keterangan = "Operator Verified"
			# 		)
			# 		riwayat_.save()

			# 		data = {'success': True,
			# 				'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
			# 				'data': {}}
			# 		response = HttpResponse(json.dumps(data))
			# else:
			# 	p = pembayaran.save(commit=False)
			# 	p.save()
			# 	p.pengajuan_izin.status = 5
			# 	p.pengajuan_izin.save()
			# 	riwayat_ = Riwayat(
			# 		pengajuan_izin_id = p.pengajuan_izin.id,
			# 		created_by_id = request.user.id,
			# 		keterangan = "Operator Verified"
			# 	)
			# 	riwayat_.save()

			# 	data = {'success': True,
			# 			'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
			# 			'data': {}}
			# 	response = HttpResponse(json.dumps(data))
		else:
			data = pembayaran.errors.as_json()
			response = HttpResponse(data)
	else:
		data = {'success': False,
						'pesan': 'Terjadi Kesalahan Pengajuan Tidak Ditemukan',
						'data': {}}
		response = HttpResponse(json.dumps(data))
	return response