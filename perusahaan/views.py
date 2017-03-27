# from django.shortcuts import render
# from django.http import HttpResponse
# from perusahaan.forms import AktaNotarisForm
# from perusahaan.models import KBLI

# # Create your views here.
# def index(request):
#     if request.method == 'POST':
#         aktaform = AktaNotarisForm(request.POST)
#         if aktaform.is_valid():
#             return HttpResponseRedirect('/suwun/')
#     else:
#         aktaform = AktaNotarisForm()
#     return render(request, 'index.html', {'aktaform': aktaform})

# def index(request, extra_context={}):
	
# 	siswa=Siswa.objects.all()

# 	extra_context.update({'siswa':siswa})


# 	return render(request, "front_end/index.html", extra_context)


# def tambah(request, extra_context={}):
# 	if request.method == 'POST':
# 		form= Siswaform(request.POST)
# 		if form.is_valid():
# 			sekolah = form.cleaned_data['sekolah']
# 			no_pendaftaran = form.cleaned_data['no_pendaftaran']
# 			#no_peserta = form.cleaned_data['no_peserta']
# 			no_ujian = form.cleaned_data['no_ujian']
# 			nisn = form.cleaned_data['nisn']
# 			nama_siswa= form.cleaned_data['nama_siswa']
# 			jk = form.cleaned_data['jk']
# 			tempat_lahir = form.cleaned_data['tempat_lahir']
# 			tanggal_lahir = form.cleaned_data['tanggal_lahir']
# 			asalsekolah = form.cleaned_data['asalsekolah']
# 			nilai_ind = form.cleaned_data['nilai_ind']
# 			nilai_mat= form.cleaned_data['nilai_mat']
# 			nilai_eng = form.cleaned_data['nilai_eng']
# 			nilai_ipa = form.cleaned_data['nilai_ipa']
# 			lokasi_daftar = form.cleaned_data['lokasi_daftar']

# 			simpan_siswa= form.save(commit=False)
			
# 			simpan_siswa.sekolah=sekolah
# 			simpan_siswa.no_pendaftaran=no_pendaftaran
# 			tgl = (tanggal_lahir.strftime('%Y%m%d'))
# 			nisn_ = str(nisn)
# 			no_peserta_ = tgl+nisn_
# 			# print int(no_peserta_)
# 			simpan_siswa.no_peserta=int(no_peserta_)
# 			simpan_siswa.no_ujian=no_ujian
# 			simpan_siswa.nisn=nisn
# 			simpan_siswa.nama_siswa=nama_siswa
# 			simpan_siswa.jk=jk
# 			simpan_siswa.tempat_lahir=tempat_lahir
# 			simpan_siswa.tanggal_lahir=tanggal_lahir
# 			simpan_siswa.asalsekolah=asalsekolah
# 			simpan_siswa.nilai_ind=nilai_ind
# 			simpan_siswa.nilai_mat=nilai_mat
# 			simpan_siswa.nilai_eng=nilai_eng
# 			simpan_siswa.nilai_ipa=nilai_ipa
# 			simpan_siswa.lokasi_daftar=lokasi_daftar
# 			simpan_siswa.save()
# 			return HttpResponse("You're looking at question")
		
# 	else :
# 		form= Siswaform()
# 	extra_context.update({'form':form})
# 	return render(request, "front_end/tambah.html", extra_context)

from izin.models import DetilSIUP
from izin.utils import formatrupiah

def editkekayaan():
    a = DetilSIUP.objects.all()
    try:
        for b in a:
            if b.kekayaan_bersih:
                o = b.kekayaan_bersih.split('.')
                b.kekayaan_bersih = formatrupiah(o[0])
                b.save()
                print b.kekayaan_bersih
            else:
                print "kosong"
    except AttributeError:
        print 'error'


def editsaham():
    a = DetilSIUP.objects.all()
    try:
        for b in a:
            if b.total_nilai_saham:
                o = b.total_nilai_saham.split('.')
                b.total_nilai_saham = formatrupiah(o[0])
                b.save()
                print b.total_nilai_saham
            else:
                print "kosong"
    except AttributeError:
        print 'error'

