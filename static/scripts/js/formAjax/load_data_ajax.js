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
            load_desa_imb_reklame(respon.data.id_kecamatan)
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