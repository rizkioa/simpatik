function load_pemohon(ktp_){
    if (ktp_ !== ""){
        $(".tab-content").mLoading();
        csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: 'POST',
            url: __base_url__+'/load-pemohon/'+ktp_,
            data: { csrfmiddlewaretoken: csrf_token },
            success: function (data) {
                respon = $.parseJSON(data)
                if(respon.success === true){
                    setTimeout(function(){
                        $('#id_negara').val(respon.data.negara).prop('selected',true).trigger("chosen:updated");
                    }, 1000);
                    load_provinsi(respon.data.negara)
                    setTimeout(function(){
                        $('#id_provinsi').val(respon.data.provinsi).prop('selected',true).trigger("chosen:updated");
                    }, 1000);
                    load_kabupaten(respon.data.provinsi)
                    setTimeout(function(){
                        $('#id_kabupaten').val(respon.data.kabupaten).prop('selected',true).trigger("chosen:updated")
                    }, 1000);
                    load_kecamatan(respon.data.kabupaten)
                    setTimeout(function(){
                        $('#id_kecamatan').val(respon.data.kecamatan).prop('selected',true).trigger("chosen:updated");
                    }, 1000);
                    load_desa(respon.data.kecamatan)
                    setTimeout(function(){
                        $('#id_desa').val(respon.data.desa).prop('selected',true).trigger("chosen:updated");
                    }, 1000);
                    
                    $('#id_paspor').val(respon.data.paspor);
                    // $('#id_jabatan_pemohon').val(respon.data.jabatan_pemohon);
                    $('#id_nama_lengkap').val(respon.data.nama_lengkap);
                    $('#id_tempat_lahir').val(respon.data.tempat_lahir);
                    $('#id_tanggal_lahir').val(respon.data.tanggal_lahir);
                    $('#alamat_pemohon_load').val(respon.data.alamat);
                    $('#no_telepon_pemohon_load').val(respon.data.telephone);
                    $('#hp_load').val(respon.data.hp);
                    $('#email_pemohon_load').val(respon.data.email);
                    $('#kewarganegaraan_pemohon_load').val(respon.data.kewarganegaraan).prop('selected',true).trigger("chosen:updated");
                    $('#pekerjaan_pemohon_load').val(respon.data.pekerjaan).prop('selected',true).trigger("chosen:updated");
                    $('#id_keterangan_pekerjaan').val(respon.data.keterangan_pekerjaan).prop('selected',true).trigger("chosen:updated");
                    
                }
                else{
                    $('#id_nama_lengkap').val("");
                    $('#id_tempat_lahir').val("");
                    $('#id_tanggal_lahir').val("");
                    $('#id_paspor').val("");
                    $('#id_tempat_lahir').val("");
                    $('#id_tanggal_lahir').val("");
                    $('#alamat_pemohon_load').val("");
                    $('#no_telepon_pemohon_load').val("");
                    $('#hp_load').val("");
                    $('#email_pemohon_load').val("");
                    $('#kewarganegaraan_pemohon_load').val("").prop('selected',true).trigger("chosen:updated");
                    $('#pekerjaan_pemohon_load').val("").prop('selected',true).trigger("chosen:updated");
                    $('#id_keterangan_pekerjaan').val("").prop('selected',true).trigger("chosen:updated");
                    if ($.cookie('id_pemohon') === "0"){
                        $('#id_negara').val("").prop('selected',true).trigger("chosen:updated");
                        $('#id_provinsi').val("").prop('selected',true).trigger("chosen:updated");
                        $('#id_kabupaten').val("").prop('selected',true).trigger("chosen:updated")
                        $('#id_kecamatan').val("").prop('selected',true).trigger("chosen:updated");
                        $('#id_desa').val("").prop('selected',true).trigger("chosen:updated");
                    }
                    
                    $('#id_negara').val('1').prop('selected',true).trigger("chosen:updated");
                    load_provinsi('1')
                    load_kabupaten('1')
                    load_kecamatan('1083')
                    setTimeout(function(){
                        $('#id_provinsi').val('1').prop('selected',true).trigger("chosen:updated");
                        $('#id_kabupaten').val('1083').prop('selected',true).trigger("chosen:updated")
                    }, 1000);
                }
                $(".tab-content").mLoading('hide');
            },
            error: function(data) {
                toastr["error"]("Terjadi kesalahan pada koneksi server. Coba reload ulang browser Anda. ")
                $(".tab-content").mLoading('hide');
            }
        });
    }
}

function make_disabled(elem_, dis_){
    if (dis_ == true){
        elem_.empty();
    }
    elem_.prop( "disabled", dis_);
    elem_.trigger("chosen:updated");
}

function load_provinsi(id_negara){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_provinsi_chosen" ).mLoading();
    // $( "#id_provinsi_chosen .loadmask-msg" ).css('top', '2px')
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, negara: id_negara }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_provinsi' %}', // the file to call
        url: __base_url__+'/admin/master/provinsi/option/',
        success: function(response) { // on success..
            elem = $( "#id_provinsi" )
            elem.html(response);
            make_disabled(elem, false)
            // $( "#id_provinsi_chosen" ).unmask()
            $( "#id_provinsi_chosen" ).mLoading('hide');
            $( "#id_provinsi" ).change(function(){
                $this = $(this)
                id_provinsi = $(this).val()
                if(id_provinsi.length > 0){
                    load_kabupaten(id_provinsi)
                }else{
                    elem = $( "#id_kabupaten" )
                    make_disabled(elem, true)
                }
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}
make_disabled($( "#id_provinsi" ), true)
make_disabled($( "#id_kabupaten" ), true)
make_disabled($( "#id_kecamatan" ), true)
make_disabled($( "#id_desa" ), true)
$( "#id_negara" ).change(function(){
    $this = $(this)
    id_negara = $(this).val()
    if(id_negara.length > 0){
        load_provinsi(id_negara)
        make_disabled($( "#id_provinsi" ), true)
        make_disabled($( "#id_kabupaten" ), true)
        make_disabled($( "#id_kecamatan" ), true)
        make_disabled($( "#id_desa" ), true)
    }else{
        make_disabled($( "#id_provinsi" ), true)
        make_disabled($( "#id_kabupaten" ), true)
        make_disabled($( "#id_kecamatan" ), true)
        make_disabled($( "#id_desa" ), true)
    }
})
function load_kabupaten(id_provinsi){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_kabupaten_chosen" ).mLoading();
    $( "#id_kabupaten_chosen .loadmask-msg" ).css('top', '2px')
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, provinsi: id_provinsi }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_kabupaten' %}',
        url: __base_url__+'/admin/master/kabupaten/option/',
        success: function(response) { // on success..
            elem = $( "#id_kabupaten" )
            elem.html(response);
            make_disabled(elem, false)
            $( "#id_kabupaten_chosen" ).mLoading('hide');
            $( "#id_kabupaten" ).change(function(){
                $this = $(this)
                id_kabupaten = $(this).val()
                if(id_kabupaten.length > 0){
                    load_kecamatan(id_kabupaten)
                }else{
                    elem = $( "#id_kecamatan" )
                    make_disabled(elem, true)
                }
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}
function load_kecamatan(id_kabupaten){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_kecamatan_chosen" ).mLoading();
    $( "#id_kecamatan_chosen .loadmask-msg" ).css('top', '2px')
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kabupaten: id_kabupaten }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_kecamatan' %}', // the file to call
        url: __base_url__+'/admin/master/kecamatan/option/',
        success: function(response) { // on success..
            elem = $( "#id_kecamatan" )
            elem.html(response);
            make_disabled(elem, false)
            $( "#id_kecamatan_chosen" ).mLoading('hide');
            $( "#id_kecamatan" ).change(function(){
                $this = $(this)
                
                id_kecamatan = $(this).val()
                if(id_kecamatan.length > 0){
                    load_desa(id_kecamatan)
                }else{
                    elem = $( "#id_desa" )
                    make_disabled(elem, true)
                }
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}
function load_desa(id_kecamatan){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_desa_chosen" ).mLoading();
    $( "#id_desa_chosen .loadmask-msg" ).css('top', '2px')
    $.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kecamatan: id_kecamatan }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_desa' %}', // the file to call
        url: __base_url__+'/admin/master/desa/option/',
        success: function(response) { // on success..
            elem = $( "#id_desa" )
            elem.html(response);
            make_disabled(elem, false)
            $( "#id_desa_chosen" ).mLoading('hide');
            $( "#id_desa" ).change(function(){
                $this = $(this)
            })
        },
        error: function(data) {                
            toast_server_error()
        }
    });
}

id_pengajuan = $.cookie('id_pengajuan');
if (id_pengajuan == '0'){
  $('#id_negara').val('1').prop('selected',true).trigger("chosen:updated");
  load_provinsi('1')
  load_kabupaten('1')
  load_kecamatan('1083')
  setTimeout(function(){
    $('#id_provinsi').val('1').prop('selected',true).trigger("chosen:updated");
    $('#id_kabupaten').val('1083').prop('selected',true).trigger("chosen:updated")
  }, 1000);
}