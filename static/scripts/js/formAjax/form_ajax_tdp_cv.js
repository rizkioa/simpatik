$('.kuasa_disable').prop('disabled', true).trigger("chosen:updated");
$("#switch_pemohon_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.kuasa_disable').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.kuasa_disable').prop('disabled', true).trigger("chosen:updated");
  }
});

$('.data_umum_kantor_cabang').prop('disabled', true).trigger("chosen:updated");
$("#switch_data_umum_kantor_cabang_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.data_umum_kantor_cabang').prop('disabled', false).trigger("chosen:updated");
    load_provinsi_(1, '#id_provinsi-3')
  }
  else {
    $('.data_umum_kantor_cabang').prop('disabled', true).trigger("chosen:updated");
  }
});

$('.stap3_bagian_unit').prop('disabled', true).trigger("chosen:updated");
$("#switch_stap3_bagi_unit_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.stap3_bagian_unit').prop('disabled', false).trigger("chosen:updated");
    load_provinsi_(1, '#id_provinsi-4');
  }
  else {
    $('.stap3_bagian_unit').prop('disabled', true).trigger("chosen:updated");
  }
});


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
      url: __base_url__+'/ajax-load-berkas-tdp/'+id_pengajuan,
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