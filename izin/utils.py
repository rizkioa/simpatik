JENIS_IZIN = (
	('Izin Daerah', 'IZIN DAERAH'),
	('Izin Penanaman Modal', 'IZIN PENANAMAN MODAL'),
	('Izin Pembangunan', 'IZIN PEMBANGUNAN'),
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

JENIS_IUJK = (
	('IUJK Pelaksana Kontruksi', 'IUJK Pelaksana Kontruksi'),
	('IUJK Perencana Kontruksi', 'IUJK Perencana Kontruksi'),
	('IUJK Pengawas Kontruksi', 'IUJK Pengawas Kontruksi'),
)

JENIS_ANGGOTA_BADAN_USAHA = (
	('Direktur / Penanggung Jawab Badan Usaha', 'Direktur / Penanggung Jawab Badan Usaha'),
	('Penanggung Jawab Teknik Badan Usaha', 'Penanggung Jawab Teknik Badan Usaha'),
	('Tenaga Non Teknik', 'Tenaga Non Teknik'),
)

def terbilang_(bil):
	satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh','delapan', 'sembilan', 'sepuluh', 'sebelas']
	Hasil = " "
	n = int(bil)
	if n >= 0 and n <= 11:
		hasil = [satuan[n]]
	elif n >= 12 and n <= 19:
		hasil = terbilang_(n % 10) + ['belas']
	elif n >= 20 and n <= 99:
		hasil = terbilang_(n / 10) + ['puluh'] + terbilang_(n % 10)
	elif n >= 100 and n <= 199:
		hasil = ['seratus'] + terbilang_(n - 100)
	elif n >= 200 and n <= 999:
		hasil = terbilang_(n / 100) + ['ratus'] + terbilang_(n % 100)
	elif n >= 1000 and n <= 1999:
		hasil = ['seribu'] + terbilang_(n - 1000)
	elif n >= 2000 and n <= 999999:
		hasil = terbilang_(n / 1000) + ['ribu'] + terbilang_(n % 1000)
	elif n >= 1000000 and n <= 999999999:
		hasil = terbilang_(n / 1000000) + ['juta'] + terbilang_(n % 1000000)
	else:
		hasil = terbilang_(n / 1000000000) + ['milyar'] + terbilang_(n % 100000000)
	return hasil


def terbilang(n):
	if n == 0:
		return 'nol'
	t = terbilang_(n)
	while '' in t:
		t.remove('')
	return ' '.join(t)

if __name__ == '__main__':        
	n = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 19, 20, 21, 50, 99, 100, 102,
		 989, 1000, 1001, 9891, 10000, 100000, 200001, 987123, 1000000,
		 10000000, 10000000000]
		 
	for i in n:
		s = '{:,}'.format(i)
	print('{i} -> {t}'.format(i=s, t=terbilang(i)))

def formatrupiah(uang):
	i = int(uang)
	y = str(i)
	if len(y) <= 3 :
		return 'Rp ' + y     
	else :
		p = y[-3:]
		q = y[:-3]
		return   formatrupiah(q) + '.' + p