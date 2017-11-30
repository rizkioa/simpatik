from models import MerkTypeKendaraan
import csv

def import_kbli():
    f1 = file('static/import/dishub/merk_type_mobile.csv', 'r') 

    c1 = csv.reader(f1) # Data 
    row = 0 
    for kl in c1:
        row += 1
        print kl[0]
        nama_merk = kl[0]

        # print "Baris => "+str(row)

        k, created = MerkTypeKendaraan.objects.get_or_create(nama_type=nama_merk)
        k.save()
        # # k.nama_kbli = nama_kbli
        # k.keterangan = keterangan
        # k.versi = versi
        # k.save()
        # print "simpan "+str(k.nama_kbli)+' kode kbli '+str(k.kode_kbli)
    print row
    print "######################## DONE ########################"