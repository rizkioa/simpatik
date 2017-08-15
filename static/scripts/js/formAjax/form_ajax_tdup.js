$('.akta_pendirian_disable').prop('disabled', true).trigger("chosen:updated");
$('#form-akta_pendirian').hide()
$("#switch_akta_pendirian_disabled").change(function() {
	if ($(this).is(':checked')) {
		$('.akta_pendirian_disable').prop('disabled', false).trigger("chosen:updated");
		$('#form-akta_pendirian').show()
	}
	else {
		$('.akta_pendirian_disable').prop('disabled', true).trigger("chosen:updated");
		$('#form-akta_pendirian').hide()
	}
});

$('.akta_perubahan_disable').prop('disabled', true).trigger("chosen:updated");
$('#form-akta_perubahan').hide()
$("#switch_akta_perubahan_disabled").change(function() {
	if ($(this).is(':checked')) {
		$('.akta_perubahan_disable').prop('disabled', false).trigger("chosen:updated");
		$('#form-akta_perubahan').show()

	}
	else {
		$('.akta_perubahan_disable').prop('disabled', true).trigger("chosen:updated");
		$('#form-akta_perubahan').hide()

	}
});

$('.kuasa_disable').prop('disabled', true).trigger("chosen:updated");
$("#switch_pemohon_disabled").change(function() {
	if ($(this).is(':checked')) {
		$('.kuasa_disable').prop('disabled', false).trigger("chosen:updated");
	}
	else {
		$('.kuasa_disable').prop('disabled', true).trigger("chosen:updated");
	}
});

make_disabled($( "#id_kabupaten-3" ), true)
make_disabled($( "#id_kecamatan-3" ), true)
make_disabled($( "#id_desa-3" ), true)

$( "#id_provinsi-3" ).change(function(){
    $this = $(this)

    id_provinsi = $(this).val()
    if(id_provinsi.length > 0){
        load_kabupaten_(id_provinsi, '#id_kabupaten-3')
    }
    make_disabled($( "#id_kabupaten-3" ), true)
    make_disabled($( "#id_kecamatan-3" ), true)
    make_disabled($( "#id_desa-3" ), true)
})

function load_provinsi_(id_negara, elem_){
    id_negara = parseInt(id_negara)
    var elem_ = elem_
    // console.log(elem_)
    var split_ = elem_.split('-')[1]
    $('#id_provinsi-'+split_+'_chosen').mLoading();
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, negara: id_negara }, // get the form data
        type: 'POST', // GET or POST
        url: __base_url__+'/admin/master/provinsi/option/',
        success: function(response) { // on success..
            elem = $('#id_provinsi-'+split_)
            elem.html(response);
            make_disabled(elem, false)
            $('#id_provinsi-'+split_+'_chosen').mLoading('hide');
            $( '#id_provinsi-'+split_ ).change(function(){
                $this = $(this)
                id_provinsi = $(this).val()
                if(id_provinsi.length > 0){
                    load_kabupaten_(id_provinsi, '#id_kabupaten-'+split_)
                }else{
                    elem = $( '#id_provinsi-'+split_ )
                    make_disabled(elem, true)
                }
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}

function load_kabupaten_(id_provinsi, elem_){
    id_provinsi = parseInt(id_provinsi)
    var split_ = elem_.split('-')[1]
    $('#id_kabupaten-'+split_+'_chosen').mLoading();
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, provinsi: id_provinsi }, // get the form data
        type: 'POST', // GET or POST
        url: __base_url__+'/admin/master/kabupaten/option/',
        success: function(response) { // on success..
            elem = $('#id_kabupaten-'+split_)
            elem.html(response);
            make_disabled(elem, false)
            $('#id_kabupaten-'+split_+'_chosen').mLoading('hide');
            $( '#id_kabupaten-'+split_ ).change(function(){
                $this = $(this)
                id_kabupaten = $(this).val()
                if(id_kabupaten.length > 0){
                    load_kecamatan_(id_kabupaten, '#id_kecamatan-'+split_)
                }else{
                    elem = $( '#id_kabupaten-'+split_ )
                    make_disabled(elem, true)
                }
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}


function load_kecamatan_(id_kabupaten, elem_){
    id_kabupaten = parseInt(id_kabupaten)
    var split_ = elem_.split('-')[1]
    $('#id_kecamatan-'+split_+'_chosen').mLoading();
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kabupaten: id_kabupaten }, // get the form data
        type: 'POST', // GET or POST
        url: __base_url__+'/admin/master/kecamatan/option/',
        success: function(response) { // on success..
            elem = $('#id_kecamatan-'+split_)
            elem.html(response);
            make_disabled(elem, false)
            $('#id_kecamatan-'+split_+'_chosen').mLoading('hide');
            $( '#id_kecamatan-'+split_ ).change(function(){
                $this = $(this)
                id_kecamatan = $(this).val()
                if(id_kecamatan.length > 0){
                    load_desa_(id_kecamatan, '#id_desa-'+split_)
                }else{
                    elem = $( '#id_kecamatan-'+split_ )
                    make_disabled(elem, true)
                }
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}

function load_desa_(id_kecamatan, elem_){
    id_kecamatan = parseInt(id_kecamatan)
    var split_ = elem_.split('-')[1]
    $('#id_desa-'+split_+'_chosen').mLoading();
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kecamatan: id_kecamatan }, // get the form data
        type: 'POST', // GET or POST
        url: __base_url__+'/admin/master/desa/option/',
        success: function(response) { // on success..
            elem = $('#id_desa-'+split_)
            elem.html(response);
            make_disabled(elem, false)
            $('#id_desa-'+split_+'_chosen').mLoading('hide');
            $( '#id_desa-'+split_ ).change(function(){
                $this = $(this)
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}

// ***** UPLOAD FORM *****
function form_upload_dokumen(elem_){
    // alert("asdasd")
  var elem_ = elem_[0].id
  // console.log(elem_)
  var split_ = elem_.split('-')[1]
  $(".tab-content").mLoading();
  var frm = $('#form-'+split_);
  // console.log(split_)
  // frm.parsley().validate();
  if (!frm.parsley().isValid()) {
    toastr["warning"]("Berkas Tidak boleh kosong!!!")
    $(".tab-content").mLoading('hide');
    return false;
  }
  else{
    frm.ajaxSubmit({
      method: 'POST',
      data: frm.serialize(),
      url: frm.attr('action'),
      beforeSend: function() {
        var percentVal = '0%';
        $('#percent-'+split_).html(percentVal);
      },
      uploadProgress: function(event, position, total, percentComplete) {
        var percentVal = percentComplete + '%';
        $('#btn-'+split_).hide();
        $('#percent-'+split_).show();
        $('#percent-'+split_).html(percentVal);
      },
      success: function(response){
        respon = $.parseJSON(response)
        if(respon.success){
              toastr["success"](respon.pesan)
              // console.log($('#'+split_+'-konfirmasi').prop('checked', true))
              var percentVal = '100%';
              $('#percent-'+split_).html(percentVal);
              if ($.cookie('id_pengajuan') != ''){
                load_berkas($.cookie('id_pengajuan'))
              }
        }
        else{
          // $('#checkbox_berkas_foto').prop('checked', false);
          if (respon["Terjadi Kesalahan"]) {
            toastr["warning"](respon["Terjadi Kesalahan"][0]['message'])
            frm.trigger('reset');
            frm.parsley().reset();
            $('#percent-'+split_).hide();
            $('#btn-'+split_).show();
          }else{
            toastr["error"]("Terjadi Kesalahan Server !!!")
            $('#percent-'+split_).hide();
            $('#btn-'+split_).show();
          }
        }
      },
      error: function(response){
        toastr["error"]("Terjadi Kesalahan Server !!!")
        $('#percent-'+split_).hide();
        $('#btn-'+split_).show();
      }
    })
  }
  $(".tab-content").mLoading('hide');
}
// ***** END *****

// ***** Load Form Upload *****
function load_berkas(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/layanan/tdup/load-berkas/ajax/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          len = respon.berkas.length
          for (var i = 0; i < len; i++) {
            // console.log(respon.berkas[i])
            // console.log(respon.elemen[i])
            // console.log(respon.id_berkas[i])
            // style="min-width: 742px;text-align: left;"
            url = '<a id="btn-load-'+respon.elemen[i]+'" class="btn btn-success btn-sm" data-toggle="popover" data-trigger="hover" data-container="body" data-placement="bottom" href="'+respon.berkas[i]+'" target="blank_"> <i class="fa fa-check"></i> '+respon.nm_berkas[i]+' </a> <a class="btn btn-danger btn-sm" onclick="delete_berkas_upload('+respon.id_berkas[i]+',\''+respon.elemen[i]+'\');return false;" > <i class="fa fa-trash"></i> Hapus</a>'
            // console.log(url)
            $('#load-'+respon.elemen[i]).html(url)
            $('#field-'+respon.elemen[i]+' .berkas_kosong').prop('required',false);
            // $('#field-'+respon.elemen[i]+' .berkas_kosong').val(__base_url__+respon.berkas[i]);
            $('#field-'+respon.elemen[i]).hide()
            $('#checkbox-'+respon.elemen[i]).prop('checked', true); 
            img = '<div id = \"image"><img src = "'+__base_url__+respon.berkas[i]+'" style="width:100px;" /></div>'
            // console.log(img)
            $('#btn-load-'+respon.elemen[i]).popover({
              trigger: "hover",
              html: true,
              content: img,
            });
          }
        }
      }
    });
  }
  $(".tab-content").mLoading('hide');
}

function delete_berkas_upload(id, elemen){
  // $('#field-'+elemen).show()
  $(".tab-content").mLoading();
  
  $.ajax({
    url: url = __base_url__+'/ajax-delete-berkas-upload-tdp/'+id+'/'+elemen,
    success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          toastr["success"](respon.pesan)
          $('#form-'+elemen)[0].reset() 
          $('#percent-'+elemen).hide()
          $('#btn-'+elemen).show()
          $('#field-'+elemen+' .berkas_kosong').prop('required',true);
          $('#field-'+elemen).show()
          $('#load-'+elemen).html('')
          $('#checkbox-'+elemen).prop('checked', false)
        }
    },
      error: function(response){
      toast_server_error()
    }
  })
  $(".tab-content").mLoading('hide');
}

// ################### jquery tdup ####################
// @@@@@@@@ hidden elemen persen di form upload
$(window).load(function() {
  var p = 'percent-'
  $('#'+p+'surat_keputusan').hide()
  $('#'+p+'ktp').hide()
  $('#'+p+'izin_tempat_usaha').hide()
  $('#'+p+'sertifikat_lahan').hide()
  $('#'+p+'izin_gangguan').hide()
  $('#'+p+'imb').hide()
  $('#'+p+'akta_pendirian').hide()
  $('#'+p+'akta_perubahan').hide()
  $('#'+p+'npwp_perusahaan').hide()
  $('#'+p+'siup').hide()
  $('#'+p+'surat_pernyataan').hide()
  $('#'+p+'dokumen_lingkungan').hide()
  $('#'+p+'izin_usaha_angkutan').hide()
  $('#'+p+'berkas_tambahan').hide()

  $('#sub_angkutan_jalan_wisata').hide()
  $('#sub_angkutan_kereta_api_wisata').hide()
  $('#sub_angkutan_sungai_dan_danau_wisata').hide()
  $('#sub_restoran').hide()
  $('#sub_rumah_makan').hide()
  $('#sub_bar').hide()
  $('#sub_kafe').hide()
  $('#sub_pusat_makanan').hide()
  $('#sub_jasa_boga').hide()

  // konfirmasi
  $('#tr-jenis_usaha_pariwisata').show()
  $('#tr-sub_jenis_usaha_pariwisata').show()

  $('#tr-sub_angkutan_jalan_wisata').hide()
  $('#tr-sub_angkutan_kereta_api_wisata').hide()
  $('#tr-sub_angkutan_sungai_dan_danau_wisata').hide()
  $('#tr-sub_restoran').hide()
  $('#tr-sub_rumah_makan').hide()
  $('#tr-sub_bar').hide()
  $('#tr-sub_kafe').hide()
  $('#tr-sub_pusat_makanan').hide()
  $('#tr-sub_jasa_boga').hide()

  make_disabled($( "#id_jenis_usaha_pariwisata" ), true)
  make_disabled($( "#id_sub_jenis_usaha_pariwisata" ), true)
  
});
// @@@@@@@ fungsi hidden elemen step 3 sub jenis @@@@@@


// @@@@@ fungsi menampilkan element sub jenis sesuai dengan id sub @@@@@
function subjenis(val){
  var subjenis = val
  if (subjenis == 29){
    $('#sub_angkutan_sungai_dan_danau_wisata').show()
  }
  else{
    $('#sub_angkutan_sungai_dan_danau_wisata').hide()
  }
  if(subjenis == 28){
    $('#sub_angkutan_kereta_api_wisata').show()
  }
  else{
    $('#sub_angkutan_kereta_api_wisata').hide()
  }
  if(subjenis == 27){
    $('#sub_angkutan_jalan_wisata').show()
  }
  else{
    $('#sub_angkutan_jalan_wisata').hide()
  }
  if(subjenis == 30){
    $('#sub_restoran').show()
  }
  else{
    $('#sub_restoran').hide()
  }
  if(subjenis == 31){
    $('#sub_rumah_makan').show()
  }
  else{
    $('#sub_rumah_makan').hide()
  }
  if(subjenis == 32){
    $('#sub_bar').show()
  }
  else{
    $('#sub_bar').hide()
  }
  if(subjenis == 33){
    $('#sub_kafe').show()
  }
  else{
    $('#sub_kafe').hide()
  }
  if(subjenis == 34){
    $('#sub_pusat_makanan').show()
  }
  else{
    $('#sub_pusat_makanan').hide()
  }
  if(subjenis == 35){
    $('#sub_jasa_boga').show()
  }
  else{
    $('#sub_jasa_boga').hide()
  }
}

// @@@@@@@@@@ set value @@@@@@@@
function set_value_data_usaha_pariwisata(pengajuan_id){
  if (pengajuan_id !== ""){
    $(".tab-content").mLoading();
    $.ajax({
      type: 'GET',
      url: __base_url__+'/layanan/tdup/data-usaha-pariwisata/ajax/'+pengajuan_id,
        success: function (data) {
          respon_data_usaha = $.parseJSON(data)
          
          if (respon_data_usaha.success){
            if (respon_data_usaha.data.bidang_usaha_pariwisata){
              load_jenis_usaha(respon_data_usaha.data.bidang_usaha_pariwisata)
            }
            if (respon_data_usaha.data.jenis_usaha_pariwisata){
              load_sub_jenis_usaha(respon_data_usaha.data.jenis_usaha_pariwisata)
            }
            setTimeout(function(){
              $('#id_bidang_usaha_pariwisata').val(respon_data_usaha.data.bidang_usaha_pariwisata).prop('selected',true).trigger("chosen:updated");
              $('#id_jenis_usaha_pariwisata').val(respon_data_usaha.data.jenis_usaha_pariwisata).prop('selected',true).trigger("chosen:updated");
              $('#id_sub_jenis_usaha_pariwisata').val(respon_data_usaha.data.sub_jenis_usaha_pariwisata).prop('selected',true).trigger("chosen:updated");
            }, 1000);
            subjenis(respon_data_usaha.data.jenis_usaha_pariwisata)
            setTimeout(function(){

              // transportasi wisata
              $('#id_jumlah_unit_angkutan_jalan').val(respon_data_usaha.data.jumlah_unit_angkutan_jalan_wisata)
              $('#id_kapasitas_angkutan_jalan_wisata').val(respon_data_usaha.data.kapasitas_angkutan_jalan_wisata)
              $('#id_jumlah_unit_angkutan_kereta_api_wisata').val(respon_data_usaha.data.jumlah_unit_angkutan_kereta_api_wisata)
              $('#id_kapasitas_angkutan_kereta_api_wisata').val(respon_data_usaha.data.kapasitas_angkutan_kereta_api_wisata)
              $('#id_jumlah_unit_angkutan_sungai_dan_danau_wisata').val(respon_data_usaha.data.jumlah_unit_angkutan_sungai_dan_danau_wisata)
              $('#id_kapasitas_angkutan_sungai_dan_danau_wisata').val(respon_data_usaha.data.kapasitas_angkutan_sungai_dan_danau_wisata)
              // $('#id_jumlah_unit_angkutan_laut_domestik_wisata').val(respon_data_usaha.data.jumlah_unit_angkutan_laut_domestik_wisata)
              // $('#id_kapasitas_angkutan_laut_domestik_wisata').val(respon_data_usaha.data.kapasitas_angkutan_laut_domestik_wisata)
              // $('#id_jumlah_unit_angkutan_laut_internasional_wisata').val(respon_data_usaha.data.jumlah_unit_angkutan_laut_internasional_wisata)
              // $('#id_kapasitas_angkutan_laut_internasional_wisata').val(respon_data_usaha.data.kapasitas_angkutan_laut_internasional_wisata)
              // makanan dan minuman
              $('#id_jumlah_kursi_restoran').val(respon_data_usaha.data.jumlah_kursi_restoran)
              $('#id_jumlah_kursi_rumah_makan').val(respon_data_usaha.data.jumlah_kursi_rumah_makan)
              $('#id_jumlah_kursi_bar').val(respon_data_usaha.data.jumlah_kursi_bar_atau_rumah_minum)
              $('#id_jumlah_kursi_kafe').val(respon_data_usaha.data.jumlah_kursi_kafe)
              $('#id_jumlah_stand_pusat_makanan').val(respon_data_usaha.data.jumlah_stand_pusat_makanan)
              $('#id_kapasitas_produksi_jasa_boga').val(respon_data_usaha.data.kapasitas_produksi_jasa_boga)
            }, 1000);
          }
          else{
            
            $( "#jenis_usaha_pariwisata" ).fadeOut().hide();
            $( "#sub_jenis_usaha_pariwisata" ).fadeOut().hide();
          }

          $(".tab-content").mLoading('hide');
        }
    });
  }
}

function set_value_keterangan_usaha(pengajuan_id){
  if (pengajuan_id !== ""){
    $(".tab-content").mLoading();
    $.ajax({
      type: 'GET',
      url: __base_url__+'/layanan/tdup/keterangan-usaha/ajax/'+pengajuan_id,
      success: function (data) {
        respon_keterangan_usaha = $.parseJSON(data)
        // console.log(respon_keterangan_usaha)
        if (respon_keterangan_usaha.success){
          $('#id_nama_usaha').val(respon_keterangan_usaha.data.nama_usaha);
          $('#id_lokasi_usaha_pariwisata').val(respon_keterangan_usaha.data.lokasi_usaha_pariwisata);
          $('#id_telephone').val(respon_keterangan_usaha.data.telephone);
          $('#id_nomor_izin_gangguan').val(respon_keterangan_usaha.data.nomor_izin_gangguan);
          $('#id_tanggal_izin_gangguan').val(respon_keterangan_usaha.data.tanggal_izin_gangguan);
          $('#id_nomor_dokumen_pengelolaan').val(respon_keterangan_usaha.data.nomor_dokumen_pengelolaan);
          $('#id_tanggal_dokumen_pengelolaan').val(respon_keterangan_usaha.data.tanggal_dokumen_pengelolaan);
          if (respon_keterangan_usaha.data.lokasi_lengkap !== ""){
            $('#id_provinsi-3').val(respon_keterangan_usaha.data.lokasi_lengkap.id_provinsi).prop('selected',true).trigger("chosen:updated");
            load_kabupaten_(respon_keterangan_usaha.data.lokasi_lengkap.id_provinsi, '#id_kabupaten-3')
            setTimeout(function(){
              $('#id_kabupaten-3').val(respon_keterangan_usaha.data.lokasi_lengkap.id_kabupaten).prop('selected',true).trigger("chosen:updated");
            }, 1000);
            load_kecamatan_(respon_keterangan_usaha.data.lokasi_lengkap.id_kabupaten, '#id_kecamatan-3')
            setTimeout(function(){
              $('#id_kecamatan-3').val(respon_keterangan_usaha.data.lokasi_lengkap.id_kecamatan).prop('selected',true).trigger("chosen:updated");
            }, 1000);
            load_desa_(respon_keterangan_usaha.data.lokasi_lengkap.id_kecamatan, '#id_desa-3')
            setTimeout(function(){
              $('#id_desa-3').val(respon_keterangan_usaha.data.lokasi_lengkap.id_desa).prop('selected',true).trigger("chosen:updated");
            }, 1000);
          }
          
        }
        $(".tab-content").mLoading('hide');
      },
      error: function(data){
        $(".tab-content").mLoading('hide');
      }
    })
  }
}
// @@@@@@@@@@ end set value @@@@@@@@
// @@@@@ funsi load sub jenis @@@@@@

$( "#id_bidang_usaha_pariwisata" ).change(function(){
  $this = $(this)
  id_bidang_usaha_pariwisata = $(this).val()
  if(id_bidang_usaha_pariwisata.length > 0){
    load_jenis_usaha(id_bidang_usaha_pariwisata)
  }else{
    make_disabled($( "#id_jenis_usaha_pariwisata" ), true)
    make_disabled($( "#id_sub_jenis_usaha_pariwisata" ), true)
    $( "#jenis_usaha_pariwisata" ).fadeOut().hide();
    $( "#sub_jenis_usaha_pariwisata" ).fadeOut().hide();
  }
})

function load_jenis_usaha(id_bidang_usaha){
  csrf_token = $("input[name='csrfmiddlewaretoken']").val();
  $( "#id_jenis_usaha_pariwisata_chosen" ).mLoading();
  $( "#id_jenis_usaha_pariwisata_chosen .loadmask-msg" ).css('top', '2px')
  $.ajax({
      data: { csrfmiddlewaretoken: csrf_token, bidang_usaha_pariwisata: id_bidang_usaha },
      type: 'POST',
      url: __base_url__+'/admin/izin/detiltdup/option-jenis-usaha/',
      success: function(response) {
        elem = $( "#id_jenis_usaha_pariwisata" )
        elem.html(response);
        make_disabled(elem, false)
        $( "#id_sub_jenis_usaha_pariwisata" ).hide()
        $( "#jenis_usaha_pariwisata" ).fadeIn().show();
        $( "#id_jenis_usaha_pariwisata_chosen" ).mLoading('hide');
        $( "#id_jenis_usaha_pariwisata" ).change(function(){
          $this = $(this)
          id_jenis_usaha = $(this).val()
          if(id_jenis_usaha.length > 0){
            load_sub_jenis_usaha(id_jenis_usaha)
          }else{
            $( "#jenis_usaha_pariwisata" ).fadeOut().hide();
          }
        })
      },
      error: function(data) {                
        toast_server_error()
      }
  });
}

function load_sub_jenis_usaha(id_jenis_usaha){
  csrf_token = $("input[name='csrfmiddlewaretoken']").val();
  $( "#id_sub_jenis_usaha_pariwisata_chosen" ).mLoading();
  $( "#id_sub_jenis_usaha_pariwisata_chosen .loadmask-msg" ).css('top', '2px')
  $.ajax({
    data: { csrfmiddlewaretoken: csrf_token, jenis_usaha_pariwisata: id_jenis_usaha },
    type: 'POST',
    url: __base_url__+'/admin/izin/detiltdup/option-sub-jenis-usaha/',
    success: function(response) { // on success..
      elem = $( "#id_sub_jenis_usaha_pariwisata" )
      elem.html(response);
      // console.log(response)
      make_disabled(elem, false)
      if (response !== '<option></option>'){
        $( "#sub_jenis_usaha_pariwisata" ).fadeIn().show()
        $( "#id_sub_jenis_usaha_pariwisata" ).change(function(){
          $this = $(this)
        })
      }
      else{
        $( "#sub_jenis_usaha_pariwisata" ).hide()
      }
      $( "#id_sub_jenis_usaha_pariwisata_chosen" ).mLoading('hide');
    },
    error: function(data) {                
      toast_server_error()
    }
  });
}
// @@@@@ end funsi load sub jenis @@@@@@

// @@@@@@ fungsi load konfirmasi @@@@@@@@
function load_konfirmasi_tdup(pengajuan_id){
  $(".tab-content").mLoading();
  $.ajax({
    type: 'GET',
    url: __base_url__+'/layanan/tdup/konfirmasi/ajax/'+pengajuan_id,
    success: function (data) {
      resp = $.parseJSON(data)
      // console.log(resp)
      if (resp[0].success){
        // Pemohon
        $('#jenis_permohonan_konfirmasi').html(resp[1].pemohon.jenis_pengajuan)
        $('#jenis_pemohon_konfirmasi').html(resp[1].pemohon.jenis_pemohon)
        $('#nomor_ktp_konfirmasi').html(resp[1].pemohon.ktp_paspor)
        $('#nama_lengkap_konfirmasi').html(resp[1].pemohon.nama_lengkap_pemohon)
        $('#alamat_konfirmasi').html(resp[1].pemohon.alamat_lengkap_pemohon)
        $('#telephone_konfirmasi').html(resp[1].pemohon.telephone_pemohon)
        $('#hp_konfirmasi').html(resp[1].pemohon.hp_pemohon)
        setTimeout(function(){
              $('#email_konfirmasi').html(resp[1].pemohon.email_pemohon)
        }, 1000);
        
        $('#kewarganegaraan_konfirmasi').html(resp[1].pemohon.kewarganegaraan_pemohon)
        $('#pekerjaan_konfirmasi').html(resp[1].pemohon.pekerjaan_pemohon)
        // kuasa
        if (resp[4].kuasa.nama_kuasa !== ''){
          $('<h5><u>KUASA</u></h5><table width="100%" border="0"><tr><td width="25%">Nama Kuasa</td><td width="5%">:</td><td width="70%">'+resp[4].kuasa.nama_kuasa+'</td></tr><tr><td width="25%">No Identitas </td><td width="5%">:</td><td width="70%">'+resp[4].kuasa.no_identitas_kuasa+'</td></tr><tr><td width="25%">Telephone </td><td width="5%">:</td><td width="70%">'+resp[4].kuasa.telephone_kuasa+'</td></tr></table>').insertAfter('#table_pemohon_konfirmasi')
        }
        // Perusahaan
        $('#npwp_konfirmasi').html(resp[2].perusahaan.npwp_perusahaan)
        $('#nama_perusahaan_konfirmasi').html(resp[2].perusahaan.nama_perusahaan)
        $('#alamat_perusahaan_konfirmasi').html(resp[2].perusahaan.alamat_lengkap_perusahaan)
        $('#kode_pos_konfirmasi').html(resp[2].perusahaan.kode_pos_perusahaan)
        $('#telepon_konfirmasi').html(resp[2].perusahaan.telephone_perusahaan)
        $('#fax_konfirmasi').html(resp[2].perusahaan.fax_perusahaan)
        setTimeout(function(){
          $('#email_perusahaan_konfirmasi').html(resp[2].perusahaan.email_perusahaan)
        }, 1000);
        load_data_legalitas_perusahaan_tdup($.cookie('id_perusahaan'))
        $(".tab-content").mLoading('hide');


        $('#bidang_usaha_pariwisata_konfirmasi').html(resp[5].data_usaha.bidang_usaha_pariwisata)
        if (resp[5].data_usaha.jenis_usaha_pariwisata){
          $('#tr-jenis_usaha_pariwisata').show()
          $('#jenis_usaha_pariwisata_konfirmasi').html(resp[5].data_usaha.jenis_usaha_pariwisata)
        }
        if (resp[5].data_usaha.sub_jenis_usaha_pariwisata){
          $('#tr-sub_jenis_usaha_pariwisata').show()
          $('#sub_jenis_usaha_pariwisata_konfirmasi').html(resp[5].data_usaha.sub_jenis_usaha_pariwisata)
        }

        if (resp[5].data_usaha.jumlah_unit_angkutan_jalan_wisata){
          $('#tr-sub_angkutan_sungai_dan_danau_wisata').show()
          $('#sub_angkutan_sungai_dan_danau_wisata_konfirmasi').html('Jumlah Unit: '+resp[5].data_usaha.jumlah_unit_angkutan_jalan_wisata+' Kapasitas: '+resp[5].data_usaha.kapasitas_angkutan_jalan_wisata)
        }
        if (resp[5].data_usaha.jumlah_unit_angkutan_kereta_api_wisata){
          $('#tr-sub_angkutan_kereta_api_wisata').show()
          $('#sub_angkutan_kereta_api_wisata_konfirmasi').html('Jumlah Unit: '+resp[5].data_usaha.jumlah_unit_angkutan_kereta_api_wisata+' Kapasitas: '+resp[5].data_usaha.kapasitas_angkutan_kereta_api_wisata)
        }
        if (resp[5].data_usaha.jumlah_unit_angkutan_sungai_dan_danau_wisata){
          $('#tr-sub_angkutan_jalan_wisata').show()
          $('#sub_angkutan_jalan_wisata_konfirmasi').html('Jumlah Unit: '+resp[5].data_usaha.jumlah_unit_angkutan_sungai_dan_danau_wisata+' Kapasitas: '+resp[5].data_usaha.kapasitas_angkutan_sungai_dan_danau_wisata)
        }
        if (resp[5].data_usaha.jumlah_kursi_restoran){
          $('#tr-sub_restoran').show()
          $('#sub_restoran_konfirmasi').html('Jumlah Kursi: '+resp[5].data_usaha.jumlah_kursi_restoran+' buah')
        }
        if (resp[5].data_usaha.jumlah_kursi_rumah_makan){
          $('#tr-sub_rumah_makan').show()
          $('#sub_rumah_makan_konfirmasi').html('Jumlah Kursi: '+resp[5].data_usaha.jumlah_kursi_rumah_makan+' buah')
        }
        if (resp[5].data_usaha.jumlah_kursi_bar_atau_rumah_minum){
          $('#tr-sub_bar').show()
          $('#sub_bar_konfirmasi').html('Jumlah Kursi: '+resp[5].data_usaha.jumlah_kursi_bar_atau_rumah_minum+' buah')
        }
        if (resp[5].data_usaha.jumlah_kursi_kafe){
          $('#tr-sub_kafe').show()
          $('#sub_kafe_konfirmasi').html('Jumlah Kursi: '+resp[5].data_usaha.jumlah_kursi_kafe+' buah')
        }
        if (resp[5].data_usaha.jumlah_stand_pusat_makanan){
          $('#tr-sub_pusat_makanan').show()
          $('#sub_pusat_makanan_konfirmasi').html('Jumlah Stand: '+resp[5].data_usaha.jumlah_stand_pusat_makanan+' buah')
        }
        if (resp[5].data_usaha.kapasitas_produksi_jasa_boga){
          $('#tr-sub_jasa_boga').show()
          $('#sub_jasa_boga_konfirmasi').html('Kapasitas produksi/pack: '+resp[5].data_usaha.kapasitas_produksi_jasa_boga+' unit/buah')
        }

        $.ajax({
          type: 'GET',
          url: __base_url__+'/layanan/tdup/pengurus-badan-usaha/load/'+pengajuan_id,
          success: function (respon) {
            // console.log(respon)
            respon = JSON.parse(respon)
            if(respon.data.length > 0){
              $.each( respon.data, function( index ) {
                row = '<tr>'
                no = index+1
                row += '<td>'+no+'</td>'
                row += '<td>'+respon.data[index].nomor_ktp+'</td>'
                row += '<td>'+respon.data[index].nama_lengkap+'</td>'
                row += '<td>'+respon.data[index].alamat+'</td>'
                if(respon.data[index].telephone != ""){
                  row += '<td>'+respon.data[index].telephone+'</td>'
                }
                else{
                  row += '<td>-</td>'
                }
                if(respon.data[index].keterangan){
                  row += '<td>'+respon.data[index].keterangan+'</td>'
                }
                else{
                  row += '<td>-</td>'
                }
                row += '</tr>'
                $('#table_pengurus_badan_usaha_konfirmasi > tbody').append(row)
              })
            }
            else{
              row = '<tr><td colspan="6" align="center">Kosong</td></tr>'
              $('#table_pengurus_badan_usaha_konfirmasi > tbody').append(row)
            }
          },
        })

        $('#nama_usaha_konfirmasi').html(resp[3].keterangan_usaha.nama_usaha)
        $('#lokasi_usaha_pariwisata_konfirmasi').html(resp[3].keterangan_usaha.lokasi_usaha_pariwisata)
        $('#telephone_usaha_konfirmasi').html(resp[3].keterangan_usaha.telephone)
        // $('#nomor_izin_gangguan_konfirmasi').html(resp[3].keterangan_usaha.nomor_izin_gangguan)
        // $('#tanggal_gangguan_konfirmasi').html(resp[3].keterangan_usaha.tanggal_izin_gangguan)
        izin_lain_json = resp[3].keterangan_usaha.izin_lain_json
        $('#konfirmasi_data_izin_lain > tbody').html('')
        if (izin_lain_json.length > 0){
          for (var i = 0; i < izin_lain_json.length; i++){
            no = i
            if(izin_lain_json.length > 1){
              no = i+1
            }
            // console.log(no)
            
            row = '<tr>'
            row += '<td width="10%" style="padding-left:10px;">'+no+'</td>'
            row += '<td width="20%">'+izin_lain_json[i].no_izin+'</td>'
            row += '<td width="20%">'+izin_lain_json[i].tanggal_izin+'</td>'
            row += '</tr>'
            $('#konfirmasi_data_izin_lain > tbody').append(row)
          }
        }
        $('#nomor_dokumen_pengelolaan_konfirmasi').html(resp[3].keterangan_usaha.nomor_dokumen_pengelolaan)
        $('#tanggal_dokumen_pengelolaan_konfirmasi').html(resp[3].keterangan_usaha.tanggal_dokumen_pengelolaan)
      }
    }
  })
}

function load_data_legalitas_perusahaan_tdup(perusahaan_id){
  if (perusahaan_id !== ""){
    $('#table_legalitas_konfirmasi').mLoading();
    $.ajax({
      type: 'GET',
      url: __base_url__+'/ajax-load-data-legalitas-perusahaan-tdp/'+perusahaan_id,
      success: function (data) {
        a = data.length
        tablekosong = '<tr><td colspan="9" align="center">Kosong/Tidak ada...!!!</td></tr>'
        $('#table_legalitas_konfirmasi > tbody').html(tablekosong)

        if(a === 0){
          $('#table_legalitas_konfirmasi > tbody > tr:first').remove()
          table = '<tr><td colspan="9" align="center">Kosong/Tidak ada...!!!</td></tr>'
          $('#table_legalitas_konfirmasi > tbody').prepend(table)
        }
        else{
          b = data.reverse()
          $('#table_legalitas_konfirmasi > tbody > tr:first').remove()
          for (var i = 0; i < a; i++){
            jenis_legalitas = b[i].jenis_legalitas
            nama_notaris = b[i].nama_notaris
            alamat = b[i].alamat
            telephone = b[i].telephone
            nomor_akta = b[i].nomor_akta
            tanggal_akta = b[i].tanggal_akta
            nomor_pengesahan = b[i].nomor_pengesahan
            tanggal_pengesahan = b[i].tanggal_pengesahan
            no = a
            if (a > 1){
              no = a-i
            }
            row = '<tr>'
            row += '<td>'+no+'</td>'
            row += '<td>'+jenis_legalitas+'</td>'
            row += '<td>'+nama_notaris+'</td>'
            row += '<td>'+alamat+'</td>'
            row += '<td>'+telephone+'</td>'
            row += '<td>'+nomor_akta+'</td>'
            row += '<td>'+tanggal_akta+'</td>'
            row += '<td>'+nomor_pengesahan+'</td>'
            row += '<td>'+tanggal_pengesahan+'</td>'
            row += '</tr>'
            $('#table_legalitas_konfirmasi > tbody').prepend(row);
          }
        }
      },
      error: function(data) {
        toastr["error"]("Terjadi kesalahan pada koneksi server. Coba reload ulang browser Anda. ")
      }
    });
    $('#table_legalitas_konfirmasi').mLoading('hide');
  }
}
// @@@@@@ fungsi load konfirmasi @@@@@@@@

// @@@@@@@ fungsi root wizard next tab @@@@@@
$(window).load(function(){
    $('#rootwizard').bootstrapWizard({
      onTabShow: function(tab, navigation, index) {
        var $total = navigation.find('li').length;
        var $current = index+1;
        if ($current == 2){
          load_kecamatan1('', '06', '35');
          // alert('aaaa')
          if ($.cookie('npwp_perusahaan') !== '0'){
            $('#id_npwp_perusahaan').val($.cookie('npwp_perusahaan'))
            setTimeout(function(){
              load_perusahaan_a($.cookie('npwp_perusahaan'))
            }, 1000);
          }
        }
        if($current == 3){
          set_value_data_usaha_pariwisata($.cookie('id_pengajuan'))
          load_pengurus_badan_usaha($.cookie('id_pengajuan'))
        }
        if($current == 4){
          load_provinsi_(1, '#id_provinsi-3')
          if ($.cookie('id_pengajuan') !== '0'){
            set_value_keterangan_usaha($.cookie('id_pengajuan'))
            load_data_izin_lain($.cookie('id_pengajuan'))
          }
        }
        if($current == 6){
          if ($.cookie('id_pengajuan') != ''){
            load_berkas($.cookie('id_pengajuan'))
          }
        }
        if($current >= $total) {
          load_konfirmasi_tdup($.cookie('id_pengajuan'))
          $('#rootwizard').find('.pager .next').hide();
          $('#rootwizard').find('.pager .finish').show();
          $('#rootwizard').find('.pager .finish').removeClass('disabled');
        } else {
          $('#rootwizard').find('.pager .next').show();
          $('#rootwizard').find('.pager .finish').hide();
        }
      },

      onNext: function(tab, navigation, index) {
        return false;
      },

      onTabClick: function(tab, navigation, index) {
        if (window.location.hostname == 'localhost'){
          return true
        }
        else{
          return false;
        }
      }
    });
});
// @@@@@@@ end fungsi root wizard next tab @@@@@@

// @@@@@@@@@ fungsi next tab @@@@@@@@
function next_tab(btn){
  var pengajuan_id = $.cookie('id_pengajuan')
  $.ajax({
    type: 'GET',
    url: __base_url__+'/cek-detil-izin/'+pengajuan_id,
    success: function (response){
      respon = $.parseJSON(response)
      if (respon.success == true){
        // console.log('berhasil')
        var index = $('#rootwizard').bootstrapWizard('currentIndex')+1;
        var frm = $('form[name="step'+ index +'"]');
        frm.parsley().validate();
        if (frm.parsley().isValid()) {
          $(".tab-content").mLoading();
          $(btn).attr('disabled', 'disabled')
          $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (response){
              // console.log('masuk ajax')
              respon = $.parseJSON(response)
                $(btn).removeAttr('disabled')
                if(respon.success){
                  toastr["success"](respon.pesan)
                  tab_index = '#rootwizard a[href="#tab'+(index+1)+'"]'
                  $(tab_index).tab('show')
                }
                else{
                  var a = Object.keys(respon);
                  for (var i = 0; i < a.length; i++){
                    var c = a[i].replace("_", " ").charAt(0).toUpperCase()
                    var field = c + a[i].replace("_", " ").slice(1)
                    toastr["error"](field+" "+respon[a[i]][0]['message'])
                    $("#"+a[i]+"").addClass("has-error");
                    $("#id_"+a[i]+"_").addClass("has-error");
                  }
                }
                $(".tab-content").mLoading('hide');
            },
            error: function(response){
              $(".tab-content").mLoading('hide');
              $(btn).removeAttr('disabled')
              toastr["error"]("Terjadi kesalahan pada koneksi server.")
            }
          });
        }
      }
      else{
        console.log('gagal')
        $.cookie('id_pengajuan', '0', {path:'/'})
        $.cookie('id_pemohon', '0', {path:'/'})
        $.cookie('id_perusahaan', '0', {path:'/'})
        $.cookie('nomor_ktp', '0', {path:'/'})
        $.cookie('nomor_paspor', '0', {path:'/'})
        $.cookie('npwp_perusahaan', '0', {path:'/'})
        $.cookie('id_perusahaan_induk', '0', {path:'/'})
        $.cookie('npwp_perusahaan_induk', '0', {path:'/'})
      }
    },
    error: function (response){
      console.log('terjadi kesalahan')
    }
  })
};
// @@@@@@@@@ end fungsi next tab @@@@@@@@

// ################### end jquery tdup ####################