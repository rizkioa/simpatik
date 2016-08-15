JENIS_IZIN = (
	('Izin Daerah', 'IZIN DAERAH'),
	('Izin Penanaman Modal', 'IZIN PENANAMAN MODAL'),
)

import datetime

def get_tahun_choices(sejak):
	tahun_list = [(x, x) for x in range(sejak, (datetime.datetime.now().year+1))]
	tahun_list.reverse()
	return tahun_list