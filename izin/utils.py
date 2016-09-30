JENIS_IZIN = (
	('Izin Daerah', 'IZIN DAERAH'),
	('Izin Penanaman Modal', 'IZIN PENANAMAN MODAL'),
)

import datetime

def get_tahun_choices(sejak):
	tahun_list = [(x, x) for x in range(sejak, (datetime.datetime.now().year+1))]
	tahun_list.reverse()
	return tahun_list

def get_nomor_pengajuan(kode_):
	now = datetime.datetime.now()
	nomor = ""
	print now.strftime("%f")[:4]
	if kode_:
		nomor += str(kode_)
		nomor += "/"+str(now.strftime("%f")[:4])
		nomor += "/"+str(now.strftime("%m"))+str(now.strftime("%d"))
		nomor += "/"+str(now.strftime("%Y"))
	return nomor