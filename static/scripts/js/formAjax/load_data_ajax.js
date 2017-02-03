function load_data_imbreklame(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/imbreklame/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
            $('#id_jenis_papan_reklame').val(respon.data.id_jenis_papan_reklame)
            $('#id_lebar').val(respon.data.id_lebar)
            $('#id_tinggi').val(respon.data.id_tinggi)
            $('#id_jumlah').val(respon.data.id_jumlah)

            $('#id_lokasi_pasang').val(respon.data.id_lokasi_pasang)
            if (respon.data.id_kecamatan != "") {
            load_desa_imb_reklame(respon.data.id_kecamatan)
            }
            setTimeout(function(){
              $('#id_klasifikasi_jalan').val(respon.data.id_klasifikasi_jalan).prop('selected',true).trigger("chosen:updated");
              $('#id_kecamatan_imb_reklame').val(respon.data.id_kecamatan).prop('selected',true).trigger("chosen:updated");
              $('#id_desa_imb_reklame').val(respon.data.id_desa).prop('selected',true).trigger("chosen:updated");
            }, 1000);

            $('#id_tinggi').val(respon.data.id_tinggi)
            $('#id_tinggi').val(respon.data.id_tinggi)
            $('#id_batas_utara').val(respon.data.id_batas_utara)
            $('#id_batas_timur').val(respon.data.id_batas_timur)
            $('#id_batas_selatan').val(respon.data.id_batas_selatan)
            $('#id_batas_barat').val(respon.data.id_batas_barat)
          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}


function load_data_imb(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/imb/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
            $('#id_bangunan').val(respon.data.nama_bangunan)
            $('#id_luas_bangunan').val(respon.data.luas_bangunan)
            $('#id_jumlah_bangunan').val(respon.data.jumlah_bangunan)
            $('#id_lokasi').val(respon.data.id_lokasi)
            if (respon.data.id_kecamatan != "") {
              load_desa_data_reklame(respon.data.id_kecamatan)
            }
            setTimeout(function(){
              $('#id_status_hak_tanah').val(respon.data.status_tanah).prop('selected',true).trigger("chosen:updated");
              $('#id_kecamatan_data_reklame').val(respon.data.id_kecamatan).prop('selected',true).trigger("chosen:updated");
              $('#id_desa_data_reklame').val(respon.data.id_desa).prop('selected',true).trigger("chosen:updated");
            }, 1000);
            $('#id_luas_tanah').val(respon.data.luas_tanah)
            $('#id_no_surat_tanah').val(respon.data.no_surat_tanah)
            $('#id_tanggal_surat_tanah').val(respon.data.tanggal_surat_tanah)

            $('#id_luas_bangunan_lama').val(respon.data.luas_bangunan_lama)
            $('#id_no_imb_lama').val(respon.data.luas_bangunan_lama)
            $('#id_tanggal_imb_lama').val(respon.data.luas_bangunan_lama)
          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}


function load_data_identifikasi_bangunan_imb(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/imb/identifikasi-bangunan/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
          if ((respon.data.kode_kontruksi_bangunan == "BK1")||(respon.data.kode_kontruksi_bangunan == "BK23")||(respon.data.kode_izin == "503.01.04/")) {
            $('#id_bobot_kegiatan_pembangunan').val(respon.data.nilai_kegiatan_pembangunan)
            $('#id_bobot_fungsi_bangunan').val(respon.data.nilai_fungsi_bangunan)
            $('#id_bobot_tingkat_kompleksitas').val(respon.data.nilai_kompleksitas_bangunan)
            $('#id_bobot_tingkat_permanensi').val(respon.data.nilai_permanensi_bangunan)
            $('#id_bobot_ketinggian_bangunan').val(respon.data.nilai_ketinggian_bangunan)
            $('#id_bobot_lokasi_bangunan').val(respon.data.nilai_letak_bangunan)
            $('#id_bobot_kepemilikan_bangunan').val(respon.data.nilai_kepemilikan_bangunan)
            $('#id_bobot_lama_penggunaan_bangunan').val(respon.data.nilai_lama_penggunaan_bangunan)

            $('#total').val(respon.data.total_biaya)
            $('#id_total_biaya').val(respon.data.total_biaya)
              if ((respon.data.id_kontruksi) != "") {
                load_bangunan(respon.data.id_kontruksi)
              }
              setTimeout(function(){
                $('#id_kontruksi').val(respon.data.id_kontruksi).prop('selected',true).trigger("chosen:updated");
                $('#id_jenis_bangunan').val(respon.data.id_jenis_bangunan).prop('selected',true).trigger("chosen:updated");
                $('#id_kegiatan_pembangunan').val(respon.data.kegiatan_pembangunan).prop('selected',true).trigger("chosen:updated");
                $('#id_fungsi_bangunan').val(respon.data.nama_fungsi_bangunan).prop('selected',true).trigger("chosen:updated");
                $('#id_tingkat_kompleksitas').val(respon.data.kompleksitas_bangunan).prop('selected',true).trigger("chosen:updated");
                $('#id_tingkat_permanensi').val(respon.data.permanensi_bangunan).prop('selected',true).trigger("chosen:updated");
                $('#id_ketinggian_bangunan').val(respon.data.ketinggian_bangunan).prop('selected',true).trigger("chosen:updated");
                $('#id_lokasi_bangunan').val(respon.data.letak_bangunan).prop('selected',true).trigger("chosen:updated");
                $('#id_kepemilikan_bangunan').val(respon.data.kepemilikan_bangunan).prop('selected',true).trigger("chosen:updated");
                $('#id_lama_penggunaan_bangunan').val(respon.data.lama_penggunaan_bangunan).prop('selected',true).trigger("chosen:updated");
                 $("#id_parameter_bangunan").css('display', 'block')
              }, 1000);
          }else if ((respon.data.kode_kontruksi_bangunan == "BK2")||(respon.data.kode_kontruksi_bangunan == "BK17")) {
              if ((respon.data.id_kontruksi) != "") {
                load_bangunan(respon.data.id_kontruksi)
              }
              setTimeout(function(){
                $('#id_kontruksi').val(respon.data.id_kontruksi).prop('selected',true).trigger("chosen:updated");
                $('#id_jenis_bangunan').val(respon.data.id_jenis_bangunan).prop('selected',true).trigger("chosen:updated");
                $(".field-panjang_bangunan").css('display', 'block')
                $('#id_panjang').addClass('required')
              }, 1000);
              $('#id_panjang').val(respon.data.id_panjang)
          }else{
              if ((respon.data.id_kontruksi) != "") {
                load_bangunan(respon.data.id_kontruksi)
              }
              setTimeout(function(){
                $('#id_kontruksi').val(respon.data.id_kontruksi).prop('selected',true).trigger("chosen:updated");
                $('#id_jenis_bangunan').val(respon.data.id_jenis_bangunan).prop('selected',true).trigger("chosen:updated");
              }, 1000);
            }
          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_data_identifikasi_jalan_imb(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/imb/identifikasi-jalan/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
            setTimeout(function(){
              $('#id_klasifikasi_jalan').val(respon.data.id_klasifikasi_jalan).prop('selected',true).trigger("chosen:updated");
              $('#id_ruang_milik_jalan').val(respon.data.id_ruang_milik_jalan).prop('selected',true).trigger("chosen:updated");
              $('#id_ruang_pengawasan_jalan').val(respon.data.id_ruang_pengawasan_jalan).prop('selected',true).trigger("chosen:updated");
            }, 1000);
          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_konfirmasi_data_identifikasi_bangunan_imb(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/imb/identifikasi-bangunan/konfirmasi/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
          if ((respon.data.kode_kontruksi_bangunan == "BK1")||(respon.data.kode_kontruksi_bangunan == "BK23")||(respon.data.kode_izin == "503.01.04/")) {
            $('#id_kontruksi_konfirmasi').text(respon.data.id_kontruksi)
            $('#id_jenis_bangunan_konfirmasi').text(respon.data.id_jenis_bangunan)

            $('#nilai_kegiatan_pembangunan_konfirmasi').text(respon.data.nilai_kegiatan_pembangunan)
            $('#nilai_fungsi_bangunan_konfirmasi').text(respon.data.nilai_fungsi_bangunan)
            $('#nilai_kompleksitas_bangunan_konfirmasi').text(respon.data.nilai_kompleksitas_bangunan)
            $('#nilai_permanensi_bangunan_konfirmasi').text(respon.data.nilai_permanensi_bangunan)
            $('#nilai_ketinggian_bangunan_konfirmasi').text(respon.data.nilai_ketinggian_bangunan)
            $('#nilai_letak_bangunan_konfirmasi').text(respon.data.nilai_letak_bangunan)
            $('#nilai_kepemilikan_bangunan_konfirmasi').text(respon.data.nilai_kepemilikan_bangunan)
            $('#nilai_lama_penggunaan_bangunan_konfirmasi').text(respon.data.nilai_lama_penggunaan_bangunan)

            $('#kegiatan_pembangunan_konfirmasi').text(respon.data.kegiatan_pembangunan)
            $('#nama_fungsi_bangunan_konfirmasi').text(respon.data.nama_fungsi_bangunan)
            $('#kompleksitas_bangunan_konfirmasi').text(respon.data.kompleksitas_bangunan)
            $('#permanensi_bangunan_konfirmasi').text(respon.data.permanensi_bangunan)
            $('#ketinggian_bangunan_konfirmasi').text(respon.data.ketinggian_bangunan)
            $('#letak_bangunan_konfirmasi').text(respon.data.letak_bangunan)
            $('#kepemilikan_bangunan_konfirmasi').text(respon.data.kepemilikan_bangunan)
            $('#lama_penggunaan_bangunan_konfirmasi').text(respon.data.lama_penggunaan_bangunan)

            $('#total_biaya_konfirmasi').text(respon.data.total_biaya)
            $(".field-konfirmasi_parameter_bangunan ").removeClass('hide')
          }else if ((respon.data.kode_kontruksi_bangunan == "BK2")||(respon.data.kode_kontruksi_bangunan == "BK17")) {
                $(".field-konfirmasi_panjang").css('display', 'block')
                $('#id_kontruksi_konfirmasi').text(respon.data.id_kontruksi)
                $('#id_jenis_bangunan_konfirmasi').text(respon.data.id_jenis_bangunan)
                $('#id_panjang_konfirmasi').text(respon.data.id_panjang)
          }else{
                $('#id_kontruksi_konfirmasi').text(respon.data.id_kontruksi)
                $('#id_jenis_bangunan_konfirmasi').text(respon.data.id_jenis_bangunan)
            }
          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_data_informasi_tanah_izin_lokasi_dan_ippt_rumah(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/informasitanah/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
          if (respon.data.kode_izin == "IPPT-Rumah"){
            $('#id_alamat').val(respon.data.id_alamat)
            $('#id_luas').val(respon.data.id_luas)
            $('#id_status_tanah').val(respon.data.id_status_tanah)
            $('#id_no_sertifikat_petak').val(respon.data.id_no_sertifikat_petak)
            $('#id_luas_sertifikat_petak').val(respon.data.id_luas_sertifikat_petak)
            $('#id_atas_nama_sertifikat_petak').val(respon.data.id_atas_nama_sertifikat_petak)
            $('#id_tahun_sertifikat').val(respon.data.id_tahun_sertifikat)

            $('#id_no_persil').val(respon.data.id_no_persil)
            $('#id_klas_persil').val(respon.data.id_klas_persil)
            $('#id_atas_nama_persil').val(respon.data.id_atas_nama_persil)
            $('#id_penggunaan_sekarang').val(respon.data.id_penggunaan_sekarang)
            $('#id_rencana_penggunaan').val(respon.data.id_rencana_penggunaan)
                    
            if (respon.data.id_kecamatan != "") {
              load_desa_data_reklame(respon.data.id_kecamatan)
            }
            setTimeout(function(){
              $('#id_kecamatan_data_reklame').val(respon.data.id_kecamatan).prop('selected',true).trigger("chosen:updated");
              $('#id_desa_data_reklame').val(respon.data.id_desa).prop('selected',true).trigger("chosen:updated");
            }, 1000);
          } 
          else if (respon.data.kode_izin == "503.07/") {
            $('#id_no_surat_kuasa').val(respon.data.id_no_surat_kuasa)
            $('#id_tanggal_surat_kuasa').val(respon.data.id_tanggal_surat_kuasa)
            $('#id_alamat').val(respon.data.id_alamat)
            $('#id_luas').val(respon.data.id_luas)
            $('#id_status_tanah').val(respon.data.id_status_tanah)

            $('#id_no_persil').val(respon.data.id_no_persil)
            $('#id_klas_persil').val(respon.data.id_klas_persil)
            $('#id_atas_nama_persil').val(respon.data.id_atas_nama_persil)
            $('#id_penggunaan_sekarang').val(respon.data.id_penggunaan_sekarang)
            $('#id_rencana_penggunaan').val(respon.data.id_rencana_penggunaan)
                    
            if (respon.data.id_kecamatan != "") {
              load_desa_data_reklame(respon.data.id_kecamatan)
            }
            setTimeout(function(){
              $('#id_kecamatan_data_reklame').val(respon.data.id_kecamatan).prop('selected',true).trigger("chosen:updated");
              $('#id_desa_data_reklame').val(respon.data.id_desa).prop('selected',true).trigger("chosen:updated");
            }, 1000);
          }     
        }
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}


function load_data_detil_ho(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ho/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
            $('#id_perkiraan_modal').val(respon.data.id_perkiraan_modal)
            $('#id_tujuan_gangguan').val(respon.data.id_tujuan_gangguan)
            $('#id_alamat').val(respon.data.id_alamat)
            if (respon.data.id_kecamatan != "") {
              load_desa_data_reklame(respon.data.id_kecamatan)
            }
            setTimeout(function(){
              $('#id_jenis_gangguan').val(respon.data.id_jenis_gangguan).prop('selected',true).trigger("chosen:updated");
              $('#id_jenis_lokasi_usaha').val(respon.data.id_jenis_lokasi_usaha).prop('selected',true).trigger("chosen:updated");
              $('#id_jenis_bangunan').val(respon.data.id_jenis_bangunan).prop('selected',true).trigger("chosen:updated");
              $('#id_kecamatan_data_reklame').val(respon.data.id_kecamatan).prop('selected',true).trigger("chosen:updated");
              $('#id_desa_data_reklame').val(respon.data.id_desa).prop('selected',true).trigger("chosen:updated");
            }, 1000);

            $('#id_bahan_baku_dan_penolong').val(respon.data.id_bahan_baku_dan_penolong)
            $('#id_proses_produksi').val(respon.data.id_proses_produksi)
            $('#id_jenis_produksi').val(respon.data.id_jenis_produksi)
            $('#id_kapasitas_produksi').val(respon.data.id_kapasitas_produksi)
            $('#id_jumlah_tenaga_kerja').val(respon.data.id_jumlah_tenaga_kerja)
            $('#id_jumlah_mesin').val(respon.data.id_jumlah_mesin)
            $('#id_merk_mesin').val(respon.data.id_merk_mesin)
            $('#id_daya').val(respon.data.id_daya)
            $('#id_kekuatan').val(respon.data.id_kekuatan)
            $('#id_luas_ruang_tempat_usaha').val(respon.data.id_luas_ruang_tempat_usaha)
            $('#id_luas_lahan_usaha').val(respon.data.id_luas_lahan_usaha)
          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}



function load_data_informasi_kekayaan(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/pemakaian-kekayaan-daerah/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
            $('#id_lokasi').val(respon.data.id_lokasi)
            if (respon.data.id_kecamatan != "") {
              load_desa_data_reklame(respon.data.id_kecamatan)
            }
            setTimeout(function(){
              $('#id_kecamatan_data_reklame').val(respon.data.id_kecamatan).prop('selected',true).trigger("chosen:updated");
              $('#id_desa_data_reklame').val(respon.data.id_desa).prop('selected',true).trigger("chosen:updated");
            }, 1000);
            $('#id_panjang').val(respon.data.id_panjang)
            $('#id_lebar').val(respon.data.id_lebar)
            $('#id_penggunaan').val(respon.data.id_penggunaan)
          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_data_tabel_sertifikat_tanah(id_sertifikat_tanah){
  if (id_sertifikat_tanah !== ""){
    $('#id_sertifikat_tanah_konfirmasi').mLoading();
    $.ajax({
      type: 'GET',
      url: __base_url__+'/informasitanah/sertifikat-tanah/load/'+id_sertifikat_tanah,
      success: function (data) {
        a = data.length
        // tablekosong = '<tr><td colspan="9" align="center">Kosong/Tidak ada...!!!</td></tr>'
        // $('#id_penggunaan_tanah_ippt > tbody').html(tablekosong)

        if(a === 0){
          $('#id_sertifikat_tanah_konfirmasi > tbody > tr:first').remove()
          table = '<tr><td colspan="9" align="center">Kosong/Tidak ada...!!!</td></tr>'
          $('#id_sertifikat_tanah_konfirmasi > tbody').prepend(table)
        }
        else{
          b = data.reverse()
          $('#id_sertifikat_tanah_konfirmasi > tbody > tr:first').remove()
          for (var i = 0; i < a; i++){
            no_sertifikat_petak = b[i].no_sertifikat_petak
            luas_sertifikat_petak = b[i].luas_sertifikat_petak
            atas_nama_sertifikat_petak = b[i].atas_nama_sertifikat_petak
            tahun_sertifikat = b[i].tahun_sertifikat
            // no = a
            // if (a > 1){
            //   no = a-i
            // }
            row = '<tr>'
            // row += '<td>'+no+'</td>'
            row += '<td>'+no_sertifikat_petak+'</td>'
            row += '<td>'+luas_sertifikat_petak+'</td>'
            row += '<td>'+atas_nama_sertifikat_petak+'</td>'
            row += '<td>'+tahun_sertifikat+'</td>'
            row += '</tr>'
            $('#id_sertifikat_tanah_konfirmasi > tbody').prepend(row);
          }
        }
      },
      error: function(data) {
        toastr["error"]("Terjadi kesalahan pada koneksi server. Coba reload ulang browser Anda. ")
      }
    });
    $('#id_sertifikat_tanah_konfirmasi').mLoading('hide');
  }
}