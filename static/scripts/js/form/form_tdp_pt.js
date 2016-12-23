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

$('.akta_perubahan_disable').prop('disabled', true).trigger("chosen:updated");
$("#switch_akta_perubahan_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.akta_perubahan_disable').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.akta_perubahan_disable').prop('disabled', true).trigger("chosen:updated");
  }
});

$('.stap5_pengesahan_menteri').prop('disabled', true).trigger("chosen:updated");
$("#switch_stap5_pengesahan_menteri_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.stap5_pengesahan_menteri').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.stap5_pengesahan_menteri').prop('disabled', true).trigger("chosen:updated");
  }
});

$('.stap5_persetujuan_menteri').prop('disabled', true).trigger("chosen:updated");
$("#switch_stap5_persetujuan_menteri_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.stap5_persetujuan_menteri').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.stap5_persetujuan_menteri').prop('disabled', true).trigger("chosen:updated");
  }
});

$('.stap5_penerima_laporan').prop('disabled', true).trigger("chosen:updated");
$("#switch_stap5_penerima_laporan_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.stap5_penerima_laporan').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.stap5_penerima_laporan').prop('disabled', true).trigger("chosen:updated");
  }
});

$('.stap5_penerima_pemberitahuan').prop('disabled', true).trigger("chosen:updated");
$("#switch_stap5_penerima_pemberitahuan_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.stap5_penerima_pemberitahuan').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.stap5_penerima_pemberitahuan').prop('disabled', true).trigger("chosen:updated");
  }
});

$('.stap6_lainnya').prop('disabled', true).trigger("chosen:updated");
$("#switch_stap6_lainnya_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.stap6_lainnya').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.stap6_lainnya').prop('disabled', true).trigger("chosen:updated");
  }
});

//++++++++ load wilayah ++++++++++
// 33333
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

// 44444444
make_disabled($( "#id_kabupaten-4" ), true)
make_disabled($( "#id_kecamatan-4" ), true)
make_disabled($( "#id_desa-4" ), true)

$( "#id_provinsi-4" ).change(function(){
    $this = $(this)

    id_provinsi = $(this).val()
    if(id_provinsi.length > 0){
        load_kabupaten_(id_provinsi, '#id_kabupaten-4')
    }
    make_disabled($( "#id_kabupaten-4" ), true)
    make_disabled($( "#id_kecamatan-4" ), true)
    make_disabled($( "#id_desa-4" ), true)

})

// 55555

make_disabled($( "#id_kabupaten-5" ), true)
make_disabled($( "#id_kecamatan-5" ), true)
make_disabled($( "#id_desa-5" ), true)

$( "#id_provinsi-5" ).change(function(){
    $this = $(this)

    id_provinsi = $(this).val()
    if(id_provinsi.length > 0){
        load_kabupaten_(id_provinsi, '#id_kabupaten-5')
    }
    make_disabled($( "#id_kabupaten-5" ), true)
    make_disabled($( "#id_kecamatan-5" ), true)
    make_disabled($( "#id_desa-5" ), true)
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

//++++++++ end load wilayah ++++++++++