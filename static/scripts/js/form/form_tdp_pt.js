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
  }
  else {
    $('.data_umum_kantor_cabang').prop('disabled', true).trigger("chosen:updated");
  }
});

$('.stap3_bagian_unit').prop('disabled', true).trigger("chosen:updated");
$("#switch_stap3_bagi_unit_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.stap3_bagian_unit').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.stap3_bagian_unit').prop('disabled', true).trigger("chosen:updated");
  }
});

$('.stap5_akta_perubahan').prop('disabled', true).trigger("chosen:updated");
$("#switch_stap5_akta_perubahan_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.stap5_akta_perubahan').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.stap5_akta_perubahan').prop('disabled', true).trigger("chosen:updated");
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
make_disabled($( "#id_kabupaten3" ), true)
make_disabled($( "#id_kecamatan3" ), true)
make_disabled($( "#id_desa3" ), true)

$( "#id_provinsi3" ).change(function(){
    $this = $(this)

    id_provinsi = $(this).val()
    if(id_provinsi.length > 0){
        load_kabupaten3(id_provinsi)
    }else{
        elem = $( "#id_kabupaten3" )
        make_disabled(elem, true)
        // make_disabled($( "#id_provinsi" ), true)
        make_disabled($( "#id_kabupaten3" ), true)
        make_disabled($( "#id_kecamatan3" ), true)
        make_disabled($( "#id_desa3" ), true)
    }
})

function load_kabupaten3(id_provinsi){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_kabupaten_chosen" ).mask('loading')
    $( "#id_kabupaten_chosen .loadmask-msg" ).css('top', '2px')
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, provinsi: id_provinsi }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_kabupaten' %}',
        url: __base_url__+'/admin/master/kabupaten/option/',
        success: function(response) { // on success..
            elem = $( "#id_kabupaten3" )
            elem.html(response);
            make_disabled(elem, false)
            $( "#id_kabupaten_chosen" ).unmask()
            $( "#id_kabupaten3" ).change(function(){
                $this = $(this)

                id_kabupaten = $(this).val()
                if(id_kabupaten.length > 0){
                    load_kecamatan3(id_kabupaten)
                }else{
                    elem = $( "#id_kecamatan3" )
                    make_disabled(elem, true)
                }
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}

function load_kecamatan3(id_kabupaten){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_kecamatan_chosen" ).mask('loading')
    $( "#id_kecamatan_chosen .loadmask-msg" ).css('top', '2px')
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kabupaten: id_kabupaten }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_kecamatan' %}', // the file to call
        url: __base_url__+'/admin/master/kecamatan/option/',
        success: function(response) { // on success..
            elem = $( "#id_kecamatan3" )
            elem.html(response);
            make_disabled(elem, false)
            $( "#id_kecamatan_chosen" ).unmask()
            $( "#id_kecamatan3" ).change(function(){
                $this = $(this)
                
                id_kecamatan = $(this).val()
                if(id_kecamatan.length > 0){
                    load_desa3(id_kecamatan)
                }else{
                    elem = $( "#id_desa3" )
                    make_disabled(elem, true)
                }
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}

function load_desa3(id_kecamatan){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_desa_chosen" ).mask('loading')
    $( "#id_desa_chosen .loadmask-msg" ).css('top', '2px')
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kecamatan: id_kecamatan }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_desa' %}', // the file to call
        url: __base_url__+'/admin/master/desa/option/',
        success: function(response) { // on success..
            elem = $( "#id_desa3" )
            elem.html(response);
            make_disabled(elem, false)
            $( "#id_desa_chosen" ).unmask()
            $( "#id_desa3" ).change(function(){
                $this = $(this)
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}

// 44444444
make_disabled($( "#id_kabupaten4" ), true)
make_disabled($( "#id_kecamatan4" ), true)
make_disabled($( "#id_desa4" ), true)

$( "#id_provinsi4" ).change(function(){
    $this = $(this)

    id_provinsi = $(this).val()
    if(id_provinsi.length > 0){
        load_kabupaten4(id_provinsi)
    }else{
        elem = $( "#id_kabupaten4" )
        make_disabled(elem, true)
        // make_disabled($( "#id_provinsi" ), true)
        make_disabled($( "#id_kabupaten4" ), true)
        make_disabled($( "#id_kecamatan4" ), true)
        make_disabled($( "#id_desa4" ), true)
    }
})

function load_kabupaten4(id_provinsi){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_kabupaten_chosen" ).mask('loading')
    $( "#id_kabupaten_chosen .loadmask-msg" ).css('top', '2px')
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, provinsi: id_provinsi }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_kabupaten' %}',
        url: __base_url__+'/admin/master/kabupaten/option/',
        success: function(response) { // on success..
            elem = $( "#id_kabupaten4" )
            elem.html(response);
            make_disabled(elem, false)
            $( "#id_kabupaten_chosen" ).unmask()
            $( "#id_kabupaten4" ).change(function(){
                $this = $(this)

                id_kabupaten = $(this).val()
                if(id_kabupaten.length > 0){
                    load_kecamatan4(id_kabupaten)
                }else{
                    elem = $( "#id_kecamatan4" )
                    make_disabled(elem, true)
                }
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}

function load_kecamatan4(id_kabupaten){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_kecamatan_chosen" ).mask('loading')
    $( "#id_kecamatan_chosen .loadmask-msg" ).css('top', '2px')
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kabupaten: id_kabupaten }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_kecamatan' %}', // the file to call
        url: __base_url__+'/admin/master/kecamatan/option/',
        success: function(response) { // on success..
            elem = $( "#id_kecamatan4" )
            elem.html(response);
            make_disabled(elem, false)
            $( "#id_kecamatan_chosen" ).unmask()
            $( "#id_kecamatan4" ).change(function(){
                $this = $(this)
                
                id_kecamatan = $(this).val()
                if(id_kecamatan.length > 0){
                    load_desa4(id_kecamatan)
                }else{
                    elem = $( "#id_desa4" )
                    make_disabled(elem, true)
                }
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}

function load_desa4(id_kecamatan){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_desa_chosen" ).mask('loading')
    $( "#id_desa_chosen .loadmask-msg" ).css('top', '2px')
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kecamatan: id_kecamatan }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_desa' %}', // the file to call
        url: __base_url__+'/admin/master/desa/option/',
        success: function(response) { // on success..
            elem = $( "#id_desa4" )
            elem.html(response);
            make_disabled(elem, false)
            $( "#id_desa_chosen" ).unmask()
            $( "#id_desa4" ).change(function(){
                $this = $(this)
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}



//++++++++ end load wilayah ++++++++++