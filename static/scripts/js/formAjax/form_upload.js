// ***** UPLOAD FORM *****
function form_upload_dokumen_informasi_kekayaan(elem_){
  var elem_ = elem_[0].id
  var split_ = elem_.split('-')[1]
  $(".tab-content").mLoading();
  var frm = $('#form-'+split_);

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
            load_berkas_informasi_kekayaan_daerah($.cookie('id_pengajuan'))
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
          toast_server_error()
          $('#percent-'+split_).hide();
          $('#btn-'+split_).show();
        }
      }
    },
    error: function(response){
      toast_server_error()
      $('#percent-'+split_).hide();
      $('#btn-'+split_).show();
    }
  })
  $(".tab-content").mLoading('hide');
}
// ***** END *****

function load_berkas_informasi_kekayaan_daerah(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ajax-load-berkas-pemakaian-kekayaan-daerah/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          len = respon.berkas.length
          for (var i = 0; i < len; i++) {
            url = '<a id="btn-load-'+respon.elemen[i]+'" class="btn btn-success btn-sm" data-toggle="popover" data-trigger="hover" data-container="body" data-placement="bottom" href="'+respon.berkas[i]+'" target="blank_"> <i class="fa fa-check"></i> '+respon.nm_berkas[i]+' </a> <a class="btn btn-danger btn-sm" onclick="delete_berkas_imb_reklame_upload('+respon.id_berkas[i]+',\''+respon.elemen[i]+'\', '+id_pengajuan+');return false;" > <i class="fa fa-trash"></i> Hapus</a>'
            $('#load-'+respon.elemen[i]).html(url)
            $('#field-'+respon.elemen[i]).hide()
            $('#checkbox-'+respon.elemen[i]).prop('checked', true); 
            img = '<div id = \"image"><img src = "'+__base_url__+respon.berkas[i]+'" style="width:100px;" /></div>'
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

function load_konfirmasi_informasi_kekayaan(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/layanan/pemakaian-kekayaan-daerah/konfirmasi/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success){
            var total = respon.data.length;
            for (var i = 0; i < total; i++){
            var key = Object.keys(respon.data[i]); // Mencari key json
            var val = respon.data[i][key[0]] // mencari value json
            var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi
            $(id).text(val);
            }
        }
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

// ***** UPLOAD FORM *****
function form_upload_dokumen_detilho(elem_){
  var elem_ = elem_[0].id
  var split_ = elem_.split('-')[1]
  $(".tab-content").mLoading();
  var frm = $('#form-'+split_);

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
            load_berkas_detilho($.cookie('id_pengajuan'))
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
          toast_server_error()
          $('#percent-'+split_).hide();
          $('#btn-'+split_).show();
        }
      }
    },
    error: function(response){
      toast_server_error()
      $('#percent-'+split_).hide();
      $('#btn-'+split_).show();
    }
  })
  $(".tab-content").mLoading('hide');
}
// ***** END *****

function load_berkas_detilho(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ajax-load-berkas-ho/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          len = respon.berkas.length
          for (var i = 0; i < len; i++) {
            url = '<a id="btn-load-'+respon.elemen[i]+'" class="btn btn-success btn-sm" data-toggle="popover" data-trigger="hover" data-container="body" data-placement="bottom" href="'+respon.berkas[i]+'" target="blank_"> <i class="fa fa-check"></i> '+respon.nm_berkas[i]+' </a> <a class="btn btn-danger btn-sm" onclick="delete_berkas_imb_reklame_upload('+respon.id_berkas[i]+',\''+respon.elemen[i]+'\', '+id_pengajuan+');return false;" > <i class="fa fa-trash"></i> Hapus</a>'
            $('#load-'+respon.elemen[i]).html(url)
            $('#field-'+respon.elemen[i]).hide()
            $('#checkbox-'+respon.elemen[i]).prop('checked', true); 
            img = '<div id = \"image"><img src = "'+__base_url__+respon.berkas[i]+'" style="width:100px;" /></div>'
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

function load_konfirmasi_detilho(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/layanan/ho/konfirmasi/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success){
            var total = respon.data.length;
            for (var i = 0; i < total; i++){
            var key = Object.keys(respon.data[i]); // Mencari key json
            var val = respon.data[i][key[0]] // mencari value json
            var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi
            $(id).text(val);
            }
        }
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

// ***** UPLOAD FORM *****
function form_upload_dokumen_izin_lokasi(elem_){
  var elem_ = elem_[0].id
  var split_ = elem_.split('-')[1]
  $(".tab-content").mLoading();
  var frm = $('#form-'+split_);

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
            load_berkas_izin_lokasi($.cookie('id_pengajuan'))
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
          toast_server_error()
          $('#percent-'+split_).hide();
          $('#btn-'+split_).show();
        }
      }
    },
    error: function(response){
      toast_server_error()
      $('#percent-'+split_).hide();
      $('#btn-'+split_).show();
    }
  })
  $(".tab-content").mLoading('hide');
}
// ***** END *****

function load_berkas_izin_lokasi(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ajax-load-berkas-izin-lokasi/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          len = respon.berkas.length
          for (var i = 0; i < len; i++) {
            url = '<a id="btn-load-'+respon.elemen[i]+'" class="btn btn-success btn-sm" data-toggle="popover" data-trigger="hover" data-container="body" data-placement="bottom" href="'+respon.berkas[i]+'" target="blank_"> <i class="fa fa-check"></i> '+respon.nm_berkas[i]+' </a> <a class="btn btn-danger btn-sm" onclick="delete_berkas_imb_reklame_upload('+respon.id_berkas[i]+',\''+respon.elemen[i]+'\', '+id_pengajuan+');return false;" > <i class="fa fa-trash"></i> Hapus</a>'
            $('#load-'+respon.elemen[i]).html(url)
            $('#field-'+respon.elemen[i]).hide()
            $('#checkbox-'+respon.elemen[i]).prop('checked', true); 
            img = '<div id = \"image"><img src = "'+__base_url__+respon.berkas[i]+'" style="width:100px;" /></div>'
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

function load_konfirmasi_izin_lokasi(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/layanan/izin-lokasi/konfirmasi/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success){
            var total = respon.data.length;
            for (var i = 0; i < total; i++){
            var key = Object.keys(respon.data[i]); // Mencari key json
            var val = respon.data[i][key[0]] // mencari value json
            var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi
            $(id).text(val);
            }
        }
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

// ***** UPLOAD FORM *****
function form_upload_dokumen_detil_huller(elem_){
  var elem_ = elem_[0].id
  var split_ = elem_.split('-')[1]
  $(".tab-content").mLoading();
  var frm = $('#form-'+split_);

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
            load_berkas_detil_huller($.cookie('id_pengajuan'))
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
          toast_server_error()
          $('#percent-'+split_).hide();
          $('#btn-'+split_).show();
        }
      }
    },
    error: function(response){
      toast_server_error()
      $('#percent-'+split_).hide();
      $('#btn-'+split_).show();
    }
  })
  $(".tab-content").mLoading('hide');
}
// ***** END *****

function load_berkas_detil_huller(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ajax-load-berkas-penggilingan-padi-&-huller/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          len = respon.berkas.length
          for (var i = 0; i < len; i++) {
            url = '<a id="btn-load-'+respon.elemen[i]+'" class="btn btn-success btn-sm" data-toggle="popover" data-trigger="hover" data-container="body" data-placement="bottom" href="'+respon.berkas[i]+'" target="blank_"> <i class="fa fa-check"></i> '+respon.nm_berkas[i]+' </a> <a class="btn btn-danger btn-sm" onclick="delete_berkas_imb_reklame_upload('+respon.id_berkas[i]+',\''+respon.elemen[i]+'\', '+id_pengajuan+');return false;" > <i class="fa fa-trash"></i> Hapus</a>'
            $('#load-'+respon.elemen[i]).html(url)
            $('#field-'+respon.elemen[i]).hide()
            $('#checkbox-'+respon.elemen[i]).prop('checked', true); 
            img = '<div id = \"image"><img src = "'+__base_url__+respon.berkas[i]+'" style="width:100px;" /></div>'
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

function load_konfirmasi_detil_huller(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/layanan/penggilingan-padi-&-huller/konfirmasi/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success){
          var jenis_pemilik = "";
          var jenis_pengusaha = "";
          var rows_hubungan = "";
          if(respon.data.pemilik_badan_usaha == false){
            jenis_pemilik = "Perorangan"
          }else{
            jenis_pemilik = "Badan Usaha"
          }
          if(respon.data.pengusaha_badan_usaha == false){
            jenis_pengusaha = "Pengusaha"
          }else{
            jenis_pengusaha = "Badan Usaha"
          }

          if(respon.data.pemilik_badan_usaha == false){
              var rows_pemilik = "";
                rows_pemilik += "<tr id=jenis_pemilik><td width=25%>Jenis Pemilik</td><td width=5%>:</td><td width=70%>"+jenis_pemilik+"</td></tr><tr><td width=25%>Nama Pemilik</td><td width=5%>:</td><td width=70%>"+respon.data.pemilik_nama_perorangan+"</td></tr><tr><td width=25%>Alamat Pemilik</td><td width=5%>:</td><td width=70%>"+respon.data.pemilik_alamat+"</td></tr>";
                $(rows_pemilik).appendTo("#pemilik","tbody");
          }
          else{
              var rows_pemilik = "";
                rows_pemilik += "<tr><td width=25%>Jenis Pemilik</td><td width=5%>:</td><td width=70%>"+jenis_pemilik+"</td></tr><tr><td width=25%>Nama Badan Usaha</td><td width=5%>:</td><td width=70%>"+respon.data.pemilik_nama_badan_usaha+"</td></tr>";
                $(rows_pemilik).appendTo("#pemilik","tbody");
          }
          if(respon.data.pengusaha_badan_usaha == false){
              var rows_pengusaha = "";
                rows_pengusaha += "<tr id=jenis_pemilik><td width=25%>Jenis Pengusaha</td><td width=5%>:</td><td width=70%>"+jenis_pengusaha+"</td></tr><tr><td width=25%>Nama Pengusaha</td><td width=5%>:</td><td width=70%>"+respon.data.pengusaha_nama_perorangan+"</td></tr><tr>      <td width=25%>Alamat Pengusaha</td><td width=5%>:</td><td width=70%>"+respon.data.pengusaha_alamat+"</td></tr>";
                $(rows_pengusaha).appendTo("#pengusaha","tbody");
          }else{
              var rows_pengusaha = "";
                rows_pengusaha += "<tr id=jenis_pemilik><td width=25%>Jenis Pengusaha</td><td width=5%>:</td><td width=70%>"+jenis_pengusaha+"</td></tr><tr><td width=25%>Nama Badan Usaha</td><td width=5%>:</td><td width=70%>"+respon.data.pengusaha_nama_badan_usaha+"</td></tr>";
                $(rows_pengusaha).appendTo("#pengusaha","tbody");
          }
          rows_hubungan += "<tr><td width=25%>Hubungan Pemilik dengan Pengusaha </td><td width=5%>:</td><td width=70%>"+respon.data.hubungan_pemilik_pengusaha+"</td></tr>";
          $(rows_hubungan).appendTo("#hubungan_pemilik_dan_pengusaha","tbody");
          

        }
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_true_false_detil_huller(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/layanan/penggilingan-padi-&-huller/true-false/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success){
            var total = respon.data.length;
            for (var i = 0; i < total; i++){
            var key = Object.keys(respon.data[i]); 
            var val = respon.data[i][key[0]] 
            var nama_id = "#"+key; 
            $(nama_id).prop('checked', val)
          }

          if($("#id_perorangan_form").is(':checked')){
              make_required($('#id_pemilik_nama_perorangan'), true)
              make_required($('#id_pemilik_alamat'), true)
              make_required($('#id_negara_perorangan'), true)
              make_required($('#id_provinsi_perorangan'), true)
              make_required($('#id_kabupaten_perorangan'), true)
              make_required($('#id_kecamatan_perorangan'), true)
              make_required($('#id_desa_perorangan'), true)
              make_required($('#id_pemilik_kewarganegaraan'), true)
              make_required($('#nama_badan_hukum_pemilik'), false)

              make_disabled($('#id_pemilik_nama_perorangan'), false)
              make_disabled($('#id_pemilik_alamat'), false)
              make_disabled($('#id_negara_perorangan'), false)
              make_disabled($('#id_provinsi_perorangan'), false)
              make_disabled($('#id_kabupaten_perorangan'), false)
              make_disabled($('#id_kecamatan_perorangan'), false)
              make_disabled($('#id_desa_perorangan'), false) 
              make_disabled($('#id_pemilik_kewarganegaraan'), false) 
              make_disabled($('#nama_badan_hukum_pemilik'), true)             
            }
          if($("#id_badan_hukum_perorangan_form").is(':checked')){
              make_disabled($('#id_pemilik_nama_perorangan'), true)
              make_disabled($('#id_pemilik_alamat'), true)
              make_disabled($('#id_negara_perorangan'), true)
              make_disabled($('#id_provinsi_perorangan'), true)
              make_disabled($('#id_kabupaten_perorangan'), true)
              make_disabled($('#id_kecamatan_perorangan'), true)
              make_disabled($('#id_desa_perorangan'), true)
              make_disabled($('#id_pemilik_kewarganegaraan'), true) 
              make_disabled($('#nama_badan_hukum_pemilik'), false)
            
              make_required($('#id_pemilik_nama_perorangan'), false)
              make_required($('#id_pemilik_alamat'), false)
              make_required($('#id_negara_perorangan'), false)
              make_required($('#id_provinsi_perorangan'), false)
              make_required($('#id_kabupaten_perorangan'), false)
              make_required($('#id_kecamatan_perorangan'), false)
              make_required($('#id_desa_perorangan'), false)
              make_required($('#id_pemilik_kewarganegaraan'), false)              
              make_required($('#nama_badan_hukum_pemilik'), true)
            }
          if($("#id_pengusaha_badan_usaha").is(':checked')){
              make_required($('#id_pengusaha_nama_perorangan'), true)
              make_required($('#id_pengusaha_alamat'), true)
              make_required($('#id_negara_pengusaha'), true)
              make_required($('#id_provinsi_pengusaha'), true)
              make_required($('#id_kabupaten_pengusaha'), true)
              make_required($('#id_kecamatan_pengusaha'), true)
              make_required($('#pengusaha_desa'), true)
              make_required($('#pengusaha_kewarganegaraan'), true)
              make_required($('#nama_badan_hukum_pengusaha'), false)

              make_disabled($('#id_pengusaha_nama_perorangan'), false)
              make_disabled($('#id_pengusaha_alamat'), false)
              make_disabled($('#id_negara_pengusaha'), false)
              make_disabled($('#id_provinsi_pengusaha'), false)
              make_disabled($('#id_kabupaten_pengusaha'), false)
              make_disabled($('#id_kecamatan_pengusaha'), false)
              make_disabled($('#pengusaha_desa'), false) 
              make_disabled($('#pengusaha_kewarganegaraan'), false) 
              make_disabled($('#nama_badan_hukum_pengusaha'), true)
            }
          if ($("#switch_badan_hukum_pengusaha").is(':checked')){
              make_disabled($('#id_pengusaha_nama_perorangan'), true)
              make_disabled($('#id_pengusaha_alamat'), true)
              make_disabled($('#id_negara_pengusaha'), true)
              make_disabled($('#id_provinsi_pengusaha'), true)
              make_disabled($('#id_kabupaten_pengusaha'), true)
              make_disabled($('#id_kecamatan_pengusaha'), true)
              make_disabled($('#pengusaha_desa'), true)
              make_disabled($('#pengusaha_kewarganegaraan'), true) 
              make_disabled($('#nama_badan_hukum_pengusaha'), false)

              make_required($('#id_pengusaha_nama_perorangan'), false)
              make_required($('#id_pengusaha_alamat'), false)
              make_required($('#id_negara_pengusaha'), false)
              make_required($('#id_provinsi_pengusaha'), false)
              make_required($('#id_kabupaten_pengusaha'), false)
              make_required($('#id_kecamatan_pengusaha'), false)
              make_required($('#pengusaha_desa'), false)
              make_required($('#pengusaha_kewarganegaraan'), false)              
              make_required($('#nama_badan_hukum_pengusaha'), true)
            }
          }
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_data_detil_huller(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/layanan/penggilingan-padi-&-huller/data/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)     
        if (respon.success){
            if($("#id_perorangan_form").is(':checked')){
              load_negara("id_negara_perorangan",respon.data.id_negara_perorangan)
              load_provinsi_huller("id_provinsi_perorangan",respon.data.id_negara_perorangan)
              load_kabupaten_huller("id_kabupaten_perorangan",respon.data.id_provinsi_perorangan)
              load_kecamatan_huller("id_kecamatan_perorangan",respon.data.id_kabupaten_perorangan)
              load_desa_huller("id_desa_perorangan",respon.data.id_kecamatan_perorangan)
              $('#id_pemilik_nama_perorangan').val(respon.data.id_pemilik_nama_perorangan)
              $('#id_pemilik_alamat').val(respon.data.id_pemilik_alamat)
              var j = respon.data.id_negara_perorangan
              if ( j == "0"){
                load_negara("id_negara_perorangan","1")
                load_provinsi_huller("id_provinsi_perorangan",'1')
                load_kabupaten_huller("id_kabupaten_perorangan",'1')
                load_kecamatan_huller("id_kecamatan_perorangan","1083")
              }else{
                setTimeout(function(){
                  $('#id_negara_perorangan').val(respon.data.id_negara_perorangan).prop('selected',true).trigger("chosen:updated");
                  $('#id_provinsi_perorangan').val(respon.data.id_provinsi_perorangan).prop('selected',true).trigger("chosen:updated");
                  $('#id_kabupaten_perorangan').val(respon.data.id_kabupaten_perorangan).prop('selected',true).trigger("chosen:updated");
                  $('#id_kecamatan_perorangan').val(respon.data.id_kecamatan_perorangan).prop('selected',true).trigger("chosen:updated");
                  $('#id_desa_perorangan').val(respon.data.id_desa_perorangan).prop('selected',true).trigger("chosen:updated");
                  $('#id_pemilik_kewarganegaraan').val(respon.data.id_pemilik_kewarganegaraan).prop('selected',true).trigger("chosen:updated");
                }, 1000);
              }
            }
            if ($("#id_badan_hukum_perorangan_form").is(':checked')){
              $('#nama_badan_hukum_pemilik').val(respon.data.nama_badan_hukum_pemilik)
            }
            if($("#id_pengusaha_badan_usaha").is(':checked')){
              load_negara("id_negara_pengusaha",respon.data.id_negara_pengusaha)
              load_provinsi_huller("id_provinsi_pengusaha",respon.data.id_negara_pengusaha)
              load_kabupaten_huller("id_kabupaten_pengusaha",respon.data.id_provinsi_pengusaha)
              load_kecamatan_huller("id_kecamatan_pengusaha",respon.data.id_kabupaten_pengusaha)
              load_desa_huller("pengusaha_desa",respon.data.id_kecamatan_pengusaha)
              $('#id_pengusaha_nama_perorangan').val(respon.data.id_pengusaha_nama_perorangan)
              $('#id_pengusaha_alamat').val(respon.data.id_pengusaha_alamat)
              var k = respon.data.id_negara_pengusaha
              if ( k == "0"){
                load_negara("id_negara_pengusaha","1")
                load_provinsi_huller("id_provinsi_pengusaha",'1')
                load_kabupaten_huller("id_kabupaten_pengusaha",'1')
                load_kecamatan_huller("id_kecamatan_pengusaha","1083")
              }else{
                setTimeout(function(){
                  $('#id_negara_pengusaha').val(respon.data.id_negara_pengusaha).prop('selected',true).trigger("chosen:updated");
                  $('#id_provinsi_pengusaha').val(respon.data.id_provinsi_pengusaha).prop('selected',true).trigger("chosen:updated");
                  $('#id_kabupaten_pengusaha').val(respon.data.id_kabupaten_pengusaha).prop('selected',true).trigger("chosen:updated");
                  $('#id_kecamatan_pengusaha').val(respon.data.id_kecamatan_pengusaha).prop('selected',true).trigger("chosen:updated");
                  $('#pengusaha_desa').val(respon.data.pengusaha_desa).prop('selected',true).trigger("chosen:updated");
                  $('#pengusaha_kewarganegaraan').val(respon.data.pengusaha_kewarganegaraan).prop('selected',true).trigger("chosen:updated");
                }, 1000);
              }
            }
            if ($("#switch_badan_hukum_pengusaha").is(':checked')){
              $('#nama_badan_hukum_pengusaha').val(respon.data.nama_badan_hukum_pengusaha)
            }
            $('#hubungan_pemilik_pengusaha').val(respon.data.hubungan_pemilik_pengusaha)
          }          
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_data_mesin_detil_huller(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/layanan/penggilingan-padi-&-huller/data-mesin-perusahaan/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success){
            var total = respon.data.length;
            for (var i = 0; i < total; i++){
            var key = Object.keys(respon.data[i]); // Mencari key json
            var val = respon.data[i][key[0]] // mencari value json
            var id = "#"+key[0] // membuat variabel id untuk sett ke id masing2 komfirmasi
            $(id).val(val);
            }
        }
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_konfirmasi_data_mesin_detil_huller(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/layanan/penggilingan-padi-&-huller/data-mesin-perusahaan/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success){
            var total = respon.data.length;
            for (var i = 0; i < total; i++){
            var key = Object.keys(respon.data[i]); // Mencari key json
            var val = respon.data[i][key[0]] // mencari value json
            var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi
            $(id).text(val);
            }
        }
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

// ***** UPLOAD FORM *****
function form_upload_dokumen_ippt_usaha(elem_){
  var elem_ = elem_[0].id
  var split_ = elem_.split('-')[1]
  $(".tab-content").mLoading();
  var frm = $('#form-'+split_);

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
          var percentVal = '100%';
          $('#percent-'+split_).html(percentVal);
          if ($.cookie('id_pengajuan') != ''){
            load_berkas_ippt_usaha($.cookie('id_pengajuan'))
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
          toast_server_error()
          $('#percent-'+split_).hide();
          $('#btn-'+split_).show();
        }
      }
    },
    error: function(response){
      toast_server_error()
      $('#percent-'+split_).hide();
      $('#btn-'+split_).show();
    }
  })
  $(".tab-content").mLoading('hide');
}
// ***** END *****
function load_berkas_ippt_usaha(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ajax-load-berkas-ippt-usaha/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          len = respon.berkas.length
          for (var i = 0; i < len; i++) {
            url = '<a id="btn-load-'+respon.elemen[i]+'" class="btn btn-success btn-sm" data-toggle="popover" data-trigger="hover" data-container="body" data-placement="bottom" href="'+respon.berkas[i]+'" target="blank_"> <i class="fa fa-check"></i> '+respon.nm_berkas[i]+' </a> <a class="btn btn-danger btn-sm" onclick="delete_berkas_imb_reklame_upload('+respon.id_berkas[i]+',\''+respon.elemen[i]+'\', '+id_pengajuan+');return false;" > <i class="fa fa-trash"></i> Hapus</a>'
            $('#load-'+respon.elemen[i]).html(url)
            $('#field-'+respon.elemen[i]).hide()
            $('#checkbox-'+respon.elemen[i]).prop('checked', true); 
            img = '<div id = \"image"><img src = "'+__base_url__+respon.berkas[i]+'" style="width:100px;" /></div>'
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

function load_data_informasi_tanah(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ippt-usaha/informasi-tanah/load/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)     
        if (respon.success){
          $('#id_no_surat_kuasa').val(respon.data.id_no_surat_kuasa)
          $('#id_tanggal_surat_kuasa').val(respon.data.id_tanggal_surat_kuasa)
          $('#id_alamat').val(respon.data.id_alamat)
          load_desa_data_reklame(respon.data.id_kecamatan)
          setTimeout(function(){
            $('#id_kecamatan_data_reklame').val(respon.data.id_kecamatan).prop('selected',true).trigger("chosen:updated");
            $('#id_desa_data_reklame').val(respon.data.id_desa).prop('selected',true).trigger("chosen:updated");
          }, 1000);
          $('#id_status_tanah').val(respon.data.id_status_tanah)
          $('#id_luas').val(respon.data.id_luas)
          $('#id_no_sertifikat_petak').val(respon.data.id_no_sertifikat_petak)
          $('#id_luas_sertifikat_petak').val(respon.data.id_luas_sertifikat_petak)
          $('#id_atas_nama_sertifikat_petak').val(respon.data.id_atas_nama_sertifikat_petak)
          $('#id_no_persil').val(respon.data.id_no_persil)
          $('#id_klas_persil').val(respon.data.id_klas_persil)
          $('#id_atas_nama_persil').val(respon.data.id_atas_nama_persil)
          $('#id_rencana_penggunaan').val(respon.data.id_rencana_penggunaan)
          $('#id_batas_utara').val(respon.data.id_batas_utara)
          $('#id_batas_timur').val(respon.data.id_batas_timur)
          $('#id_batas_selatan').val(respon.data.id_batas_selatan)
          $('#id_batas_barat').val(respon.data.id_batas_barat)
          $('#id_tanah_negara_belum_dikuasai').val(respon.data.id_tanah_negara_belum_dikuasai)
          $('#id_tanah_kas_desa_belum_dikuasai').val(respon.data.id_tanah_kas_desa_belum_dikuasai)
          $('#id_tanah_hak_pakai_belum_dikuasai').val(respon.data.id_tanah_hak_pakai_belum_dikuasai)
          $('#id_tanah_hak_guna_bangunan_belum_dikuasai').val(respon.data.id_tanah_hak_guna_bangunan_belum_dikuasai)
          $('#id_tanah_hak_milik_sertifikat_belum_dikuasai').val(respon.data.id_tanah_hak_milik_sertifikat_belum_dikuasai)
          $('#id_tanah_adat_belum_dikuasai').val(respon.data.id_tanah_adat_belum_dikuasai)
          $('#id_pemegang_hak_semula_dari_tanah_belum_dikuasai').val(respon.data.id_pemegang_hak_semula_dari_tanah_belum_dikuasai)
          $('#id_tanah_belum_dikuasai_melalui').val(respon.data.id_tanah_belum_dikuasai_melalui)
          $('#id_tanah_belum_dikuasai').val(respon.data.id_jumlah_tanah_belum_dikuasai)
          $('#id_jumlah_tanah_belum_dikuasai').val(respon.data.id_jumlah_tanah_belum_dikuasai)
          $('#id_tanah_negara_sudah_dikuasai').val(respon.data.id_tanah_negara_sudah_dikuasai)
          $('#id_tanah_kas_desa_sudah_dikuasai').val(respon.data.id_tanah_kas_desa_sudah_dikuasai)
          $('#id_tanah_hak_pakai_sudah_dikuasai').val(respon.data.id_tanah_hak_pakai_sudah_dikuasai)
          $('#id_tanah_hak_guna_bangunan_sudah_dikuasai').val(respon.data.id_tanah_hak_guna_bangunan_sudah_dikuasai)
          $('#id_tanah_hak_milik_sertifikat_sudah_dikuasai').val(respon.data.id_tanah_hak_milik_sertifikat_sudah_dikuasai)
          $('#id_tanah_adat_sudah_dikuasai').val(respon.data.id_tanah_adat_sudah_dikuasai)
          $('#id_pemegang_hak_semula_dari_tanah_sudah_dikuasai').val(respon.data.id_pemegang_hak_semula_dari_tanah_sudah_dikuasai)
          $('#id_tanah_sudah_dikuasai_melalui').val(respon.data.id_tanah_sudah_dikuasai_melalui)
          $('#id_tanah_sudah_dikuasai').val(respon.data.id_jumlah_tanah_sudah_dikuasai)
          $('#id_jumlah_tanah_sudah_dikuasai').val(respon.data.id_jumlah_tanah_sudah_dikuasai)
          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_data_rencana_pembangunan(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ippt-usaha/rencana-pembangunan/load/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
          $('#id_tipe1').val(respon.data.id_tipe1)
          $('#id_gudang1').val(respon.data.id_gudang1)
          $('#id_luas_tipe1').val(respon.data.id_luas_tipe1)
          $('#id_presentase_luas_tipe1').val(respon.data.id_presentase_luas_tipe1)
          $('#id_tipe2').val(respon.data.id_tipe2)
          $('#id_gudang2').val(respon.data.id_gudang2)
          $('#id_luas_tipe2').val(respon.data.id_luas_tipe2)
          $('#id_presentase_luas_tipe2').val(respon.data.id_presentase_luas_tipe2)
          $('#id_tipe3').val(respon.data.id_tipe3)
          $('#id_gudang3').val(respon.data.id_gudang3)
          $('#id_luas_tipe3').val(respon.data.id_luas_tipe3)
          $('#id_presentase_luas_tipe3').val(respon.data.id_presentase_luas_tipe3)
          $('#id_luas_lapangan').val(respon.data.id_luas_lapangan)
          $('#id_presentase_luas_lapangan').val(respon.data.id_luas_lapangan)
          $('#id_luas_kantor').val(respon.data.id_luas_kantor)
          $('#id_presentase_luas_kantor').val(respon.data.id_presentase_luas_kantor)
          $('#id_luas_saluran').val(respon.data.id_luas_saluran)
          $('#id_presentase_luas_saluran').val(respon.data.id_luas_saluran)
          $('#id_luas_taman').val(respon.data.id_luas_taman)
          $('#id_presentase_luas_taman').val(respon.data.id_luas_taman)
          $('#id_perincian_penggunaan_tanah').val(respon.data.id_jumlah_perincian_penggunaan_tanah)
          $('#id_jumlah_perincian_penggunaan_tanah').val(respon.data.id_jumlah_perincian_penggunaan_tanah)
          $('#id_presentase_jumlah_perincian_penggunaan_tanah').val(respon.data.id_presentase_jumlah_perincian_penggunaan_tanah)
          $('#id_presentase_perincian_penggunaan_tanah').val(respon.data.id_presentase_jumlah_perincian_penggunaan_tanah)

          $('#id_pematangan_tanah_tahap1').val(respon.data.id_pematangan_tanah_tahap1)
          $('#id_pematangan_tanah_tahap2').val(respon.data.id_pematangan_tanah_tahap2)
          $('#id_pematangan_tanah_tahap3').val(respon.data.id_pematangan_tanah_tahap3)
          $('#id_pembangunan_gedung_tahap1').val(respon.data.id_pembangunan_gedung_tahap1)
          $('#id_pembangunan_gedung_tahap2').val(respon.data.id_pembangunan_gedung_tahap2)
          $('#id_pembangunan_gedung_tahap3').val(respon.data.id_pembangunan_gedung_tahap3)
          $('#id_jangka_waktu_selesai').val(respon.data.id_jangka_waktu_selesai)

          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_data_pembiayaan_dan_pemodalan(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ippt-usaha/pembiayaan-dan-pemodalan/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
            $('#id_modal_tetap_tanah').val(respon.data.id_modal_tetap_tanah)
            $('#id_modal_tetap_bangunan').val(respon.data.id_modal_tetap_bangunan)
            $('#id_modal_tetap_mesin').val(respon.data.id_modal_tetap_mesin)
            $('#id_modal_tetap_angkutan').val(respon.data.id_modal_tetap_angkutan)
            $('#id_modal_tetap_inventaris').val(respon.data.id_modal_tetap_inventaris)          
            $('#id_modal_tetap_lainnya').val(respon.data.id_modal_tetap_lainnya)
            $('#id_modal_tetap').val(respon.data.id_jumlah_modal_tetap)
            $('#id_jumlah_modal_tetap').val(respon.data.id_jumlah_modal_tetap)

          $('#id_modal_kerja_bahan').val(respon.data.id_modal_kerja_bahan)
          $('#id_modal_kerja_gaji').val(respon.data.id_modal_kerja_gaji)
          $('#id_modal_kerja_alat_angkut').val(respon.data.id_modal_kerja_alat_angkut)
          $('#id_modal_kerja_lainnya').val(respon.data.id_modal_kerja_lainnya)
          $('#id_modal_kerja').val(respon.data.id_jumlah_modal_kerja)
          $('#id_jumlah_modal_kerja').val(respon.data.id_jumlah_modal_kerja)
          var jumlah_modal_kerja = toRp(respon.data.id_jumlah_rencana_biaya)
          $('#id_jumlah_rencana_biaya').val(jumlah_modal_kerja)


          $('#id_modal_dasar').val(respon.data.id_modal_dasar)
          $('#id_modal_ditetapkan').val(respon.data.id_modal_ditetapkan)
          $('#id_modal_disetor').val(respon.data.id_modal_disetor)
          $('#id_modal_bank_pemerintah').val(respon.data.id_modal_bank_pemerintah)
          $('#id_modal_bank_swasta').val(respon.data.id_modal_bank_swasta)
          $('#id_modal_lembaga_non_bank').val(respon.data.id_modal_lembaga_non_bank)
          $('#id_modal_pihak_ketiga').val(respon.data.id_modal_pihak_ketiga)
          var jumlah_pinjaman_dalam = toRp(respon.data.id_jumlah_pinjaman_dalam)
          $('#id_jumlah_pinjaman_dalam').val(jumlah_pinjaman_dalam)

          $('#id_modal_pinjaman_luar_negeri').val(respon.data.id_modal_pinjaman_luar_negeri)
          $('#id_investasi').val(respon.data.id_jumlah_investasi)
          $('#id_jumlah_investasi').val(respon.data.id_jumlah_investasi)


          $('#id_saham_indonesia').val(respon.data.id_saham_indonesia)
          $('#id_saham_asing').val(respon.data.id_saham_asing)
          $('#id_jumlah').val(respon.data.id_jumlah_saham)


          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_data_kebutuhan_lainnya(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ippt-usaha/kebutuhan-lainnya/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
            $('#id_tenaga_ahli').val(respon.data.id_tenaga_ahli)
            $('#id_pegawai_tetap').val(respon.data.id_pegawai_tetap)
            $('#id_pegawai_harian_tetap').val(respon.data.id_pegawai_harian_tetap)
            $('#id_pegawai_harian_tidak_tetap').val(respon.data.id_pegawai_harian_tidak_tetap)
            $('#id_kebutuhan_listrik').val(respon.data.id_kebutuhan_listrik)          
            $('#id_kebutuhan_listrik_sehari_hari').val(respon.data.id_kebutuhan_listrik_sehari_hari)
            $('#id_jumlah_daya_genset').val(respon.data.id_jumlah_daya_genset)
            $('#id_jumlah_listrik_kebutuhan_dari_pln').val(respon.data.id_jumlah_listrik_kebutuhan_dari_pln)

          $('#id_air_untuk_rumah_tangga').val(respon.data.id_air_untuk_rumah_tangga)
          $('#id_air_untuk_produksi').val(respon.data.id_air_untuk_produksi)
          $('#id_air_lainnya').val(respon.data.id_air_lainnya)
          var jumlah_kebutuhan_air = parseFloat(respon.data.id_air_untuk_rumah_tangga) + parseFloat(respon.data.id_air_untuk_produksi) + parseFloat(respon.data.id_air_lainnya)
          $('#id_jumlah_kebutuhan_air').val(jumlah_kebutuhan_air)

          $('#id_air_dari_pdam').val(respon.data.id_air_dari_pdam)
          $('#id_air_dari_sumber').val(respon.data.id_air_dari_sumber)
          $('#id_air_dari_sungai').val(respon.data.id_air_dari_sungai)
          var jumlah_minimal_kebutuhan_air = parseFloat(respon.data.id_air_dari_pdam) + parseFloat(respon.data.id_air_dari_sumber) + parseFloat(respon.data.id_air_dari_sungai)
          $('#id_jumlah_minimal_kebutuhan_air').val(jumlah_minimal_kebutuhan_air)

          $('#id_tenaga_kerja_wni').val(respon.data.id_tenaga_kerja_wni)
          $('#id_tenaga_kerja_wna').val(respon.data.id_tenaga_kerja_wna)
          $('#id_tenaga_kerja_tetap').val(respon.data.id_tenaga_kerja_tetap)
          $('#id_tenaga_kerja_tidak_tetap').val(respon.data.id_tenaga_kerja_tidak_tetap)
          var jumlah_tenaga_kerja = parseFloat(respon.data.id_tenaga_kerja_tetap) + parseFloat(respon.data.id_tenaga_kerja_tidak_tetap)
          $('#id_jumlah_tenaga_kerja').val(jumlah_tenaga_kerja)

          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_konfirmasi_informasi_tanah(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ippt-usaha/informasi-tanah/load/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success){
            $('#id_no_surat_kuasa_konfirmasi').text(respon.data.id_no_surat_kuasa);
            $('#id_tanggal_surat_kuasa_konfirmasi').text(respon.data.id_tanggal_surat_kuasa)
            $('#id_alamat_konfirmasi').text(respon.data.id_alamat)
            $('#kabupaten_konfirmasi').text(respon.data.kabupaten)
            $('#kecamatan_konfirmasi').text(respon.data.kecamatan)
            $('#desa_konfirmasi').text(respon.data.desa)
            $('#id_luas_konfirmasi').text(respon.data.id_luas)
            
            $('#id_no_sertifikat_petak_konfirmasi').text(respon.data.id_no_sertifikat_petak)
            $('#id_luas_sertifikat_petak_konfirmasi').text(respon.data.id_luas_sertifikat_petak)
            $('#id_atas_nama_sertifikat_petak_konfirmasi').text(respon.data.id_atas_nama_sertifikat_petak)
            $('#id_no_persil_konfirmasi').text(respon.data.id_no_persil)
            $('#id_klas_persil_konfirmasi').text(respon.data.id_klas_persil)
            $('#id_atas_nama_persil_konfirmasi').text(respon.data.id_atas_nama_persil)

            $('#id_rencana_penggunaan_konfirmasi').text(respon.data.id_rencana_penggunaan)
            $('#id_batas_utara_konfirmasi').text(respon.data.id_batas_utara)
            $('#id_batas_timur_konfirmasi').text(respon.data.id_batas_timur)
            $('#id_batas_selatan_konfirmasi').text(respon.data.id_batas_selatan)
            $('#id_batas_barat_konfirmasi').text(respon.data.id_batas_barat)
            $('#id_status_tanah_konfirmasi').text(respon.data.id_status_tanah)
            $('#id_tanah_negara_belum_dikuasai_konfirmasi').text(respon.data.id_tanah_negara_belum_dikuasai)
            $('#id_tanah_kas_desa_belum_dikuasai_konfirmasi').text(respon.data.id_tanah_kas_desa_belum_dikuasai)
            $('#id_tanah_hak_pakai_belum_dikuasai_konfirmasi').text(respon.data.id_tanah_hak_pakai_belum_dikuasai)
            $('#id_tanah_hak_guna_bangunan_belum_dikuasai_konfirmasi').text(respon.data.id_tanah_hak_guna_bangunan_belum_dikuasai)
            $('#id_tanah_hak_milik_sertifikat_belum_dikuasai_konfirmasi').text(respon.data.id_tanah_hak_milik_sertifikat_belum_dikuasai)
            $('#id_tanah_adat_belum_dikuasai_konfirmasi').text(respon.data.id_tanah_adat_belum_dikuasai)
            $('#id_jumlah_tanah_belum_dikuasai_konfirmasi').text(respon.data.id_jumlah_tanah_belum_dikuasai)
            $('#id_pemegang_hak_semula_dari_tanah_belum_dikuasai_konfirmasi').text(respon.data.id_pemegang_hak_semula_dari_tanah_belum_dikuasai)
            $('#id_tanah_belum_dikuasai_melalui_konfirmasi').text(respon.data.id_tanah_belum_dikuasai_melalui)
            $('#id_tanah_negara_sudah_dikuasai_konfirmasi').text(respon.data.id_tanah_negara_sudah_dikuasai)
            $('#id_tanah_kas_desa_sudah_dikuasai_konfirmasi').text(respon.data.id_tanah_kas_desa_sudah_dikuasai)
            $('#id_tanah_hak_pakai_sudah_dikuasai_konfirmasi').text(respon.data.id_tanah_hak_pakai_sudah_dikuasai)
            $('#id_tanah_hak_guna_bangunan_sudah_dikuasai_konfirmasi').text(respon.data.id_tanah_hak_guna_bangunan_sudah_dikuasai)
            $('#id_tanah_hak_milik_sertifikat_sudah_dikuasai_konfirmasi').text(respon.data.id_tanah_hak_milik_sertifikat_sudah_dikuasai)
            $('#id_tanah_adat_sudah_dikuasai_konfirmasi').text(respon.data.id_tanah_adat_sudah_dikuasai)
            $('#id_jumlah_tanah_sudah_dikuasai_konfirmasi').text(respon.data.id_jumlah_tanah_sudah_dikuasai)
            $('#id_pemegang_hak_semula_dari_tanah_sudah_dikuasai_konfirmasi').text(respon.data.id_pemegang_hak_semula_dari_tanah_sudah_dikuasai)
            $('#id_tanah_sudah_dikuasai_melalui_konfirmasi').text(respon.data.id_tanah_sudah_dikuasai_melalui)
        }
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_konfirmasi_rencana_pembangunan(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ippt-usaha/rencana-pembangunan/load/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
          $('#id_tipe1_konfirmasi').text(respon.data.id_tipe1)
          $('#id_gudang1_konfirmasi').text(respon.data.id_gudang1)
          $('#id_luas_tipe1_konfirmasi').text(respon.data.id_luas_tipe1)
          $('#id_presentase_luas_tipe1_konfirmasi').text(respon.data.id_presentase_luas_tipe1)
          $('#id_tipe2_konfirmasi').text(respon.data.id_tipe2)
          $('#id_gudang2_konfirmasi').text(respon.data.id_gudang2)
          $('#id_luas_tipe2_konfirmasi').text(respon.data.id_luas_tipe2)
          $('#id_presentase_luas_tipe2_konfirmasi').text(respon.data.id_presentase_luas_tipe2)
          $('#id_tipe3_konfirmasi').text(respon.data.id_tipe3)
          $('#id_gudang3_konfirmasi').text(respon.data.id_gudang3)
          $('#id_luas_tipe3_konfirmasi').text(respon.data.id_luas_tipe3)
          $('#id_presentase_luas_tipe3_konfirmasi').text(respon.data.id_presentase_luas_tipe3)
          $('#id_luas_lapangan_konfirmasi').text(respon.data.id_luas_lapangan)
          $('#id_presentase_luas_lapangan_konfirmasi').text(respon.data.id_luas_lapangan)
          $('#id_luas_kantor_konfirmasi').text(respon.data.id_luas_kantor)
          $('#id_presentase_luas_kantor_konfirmasi').text(respon.data.id_presentase_luas_kantor)
          $('#id_luas_saluran_konfirmasi').text(respon.data.id_luas_saluran)
          $('#id_presentase_luas_saluran_konfirmasi').text(respon.data.id_luas_saluran)
          $('#id_luas_taman_konfirmasi').text(respon.data.id_luas_taman)
          $('#id_presentase_luas_taman_konfirmasi').text(respon.data.id_luas_taman)
          $('#id_jumlah_perincian_penggunaan_tanah_konfirmasi').text(respon.data.id_jumlah_perincian_penggunaan_tanah)
          $('#id_presentase_jumlah_perincian_penggunaan_tanah_konfirmasi').text(respon.data.id_presentase_jumlah_perincian_penggunaan_tanah)

          $('#id_pematangan_tanah_tahap1_konfirmasi').text(respon.data.id_pematangan_tanah_tahap1)
          $('#id_pematangan_tanah_tahap2_konfirmasi').text(respon.data.id_pematangan_tanah_tahap2)
          $('#id_pematangan_tanah_tahap3_konfirmasi').text(respon.data.id_pematangan_tanah_tahap3)
          $('#id_pembangunan_gedung_tahap1_konfirmasi').text(respon.data.id_pembangunan_gedung_tahap1)
          $('#id_pembangunan_gedung_tahap2_konfirmasi').text(respon.data.id_pembangunan_gedung_tahap2)
          $('#id_pembangunan_gedung_tahap3_konfirmasi').text(respon.data.id_pembangunan_gedung_tahap3)
          $('#id_jangka_waktu_selesai_konfirmasi').text(respon.data.id_jangka_waktu_selesai)

          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_konfirmasi_pembiayaan_dan_pemodalan(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ippt-usaha/pembiayaan-dan-pemodalan/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
            $('#id_modal_tetap_tanah_konfirmasi').text(respon.data.id_modal_tetap_tanah)
            $('#id_modal_tetap_bangunan_konfirmasi').text(respon.data.id_modal_tetap_bangunan)
            $('#id_modal_tetap_mesin_konfirmasi').text(respon.data.id_modal_tetap_mesin)
            $('#id_modal_tetap_angkutan_konfirmasi').text(respon.data.id_modal_tetap_angkutan)
            $('#id_modal_tetap_inventaris_konfirmasi').text(respon.data.id_modal_tetap_inventaris)          
            $('#id_modal_tetap_lainnya_konfirmasi').text(respon.data.id_modal_tetap_lainnya)
            $('#id_jumlah_modal_tetap_konfirmasi').text(respon.data.id_jumlah_modal_tetap)

            $('#id_modal_kerja_bahan_konfirmasi').text(respon.data.id_modal_kerja_bahan)
            $('#id_modal_kerja_gaji_konfirmasi').text(respon.data.id_modal_kerja_gaji)
            $('#id_modal_kerja_alat_angkut_konfirmasi').text(respon.data.id_modal_kerja_alat_angkut)
            $('#id_modal_kerja_lainnya_konfirmasi').text(respon.data.id_modal_kerja_lainnya)
            $('#id_jumlah_modal_kerja_konfirmasi').text(respon.data.id_jumlah_modal_kerja)
            var jumlah_modal_kerja = toRp(respon.data.id_jumlah_rencana_biaya)
            $('#id_jumlah_rencana_biaya_konfirmasi').text(jumlah_modal_kerja)


            $('#id_modal_dasar_konfirmasi').text(respon.data.id_modal_dasar)
            $('#id_modal_ditetapkan_konfirmasi').text(respon.data.id_modal_ditetapkan)
            $('#id_modal_disetor_konfirmasi').text(respon.data.id_modal_disetor)
            $('#id_modal_bank_pemerintah_konfirmasi').text(respon.data.id_modal_bank_pemerintah)
            $('#id_modal_bank_swasta_konfirmasi').text(respon.data.id_modal_bank_swasta)
            $('#id_modal_lembaga_non_bank_konfirmasi').text(respon.data.id_modal_lembaga_non_bank)
            $('#id_modal_pihak_ketiga_konfirmasi').text(respon.data.id_modal_pihak_ketiga)
            var jumlah_pinjaman_dalam = toRp(respon.data.id_jumlah_pinjaman_dalam)
            $('#id_jumlah_pinjaman_dalam_konfirmasi').text(jumlah_pinjaman_dalam)

            $('#id_modal_pinjaman_luar_negeri_konfirmasi').text(respon.data.id_modal_pinjaman_luar_negeri)
            $('#id_jumlah_investasi_konfirmasi').text(respon.data.id_jumlah_investasi)


            $('#id_saham_indonesia_konfirmasi').text(respon.data.id_saham_indonesia)
            $('#id_saham_asing_konfirmasi').text(respon.data.id_saham_asing)
            $('#id_jumlah_konfirmasi').text(respon.data.id_jumlah_saham)


          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}

function load_konfirmasi_kebutuhan_lainnya(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ippt-usaha/kebutuhan-lainnya/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
            $('#id_tenaga_ahli_konfirmasi').text(respon.data.id_tenaga_ahli)
            $('#id_pegawai_tetap_konfirmasi').text(respon.data.id_pegawai_tetap)
            $('#id_pegawai_harian_tetap_konfirmasi').text(respon.data.id_pegawai_harian_tetap)
            $('#id_pegawai_harian_tidak_tetap_konfirmasi').text(respon.data.id_pegawai_harian_tidak_tetap)
           
            $('#id_kebutuhan_listrik_konfirmasi').text(respon.data.id_kebutuhan_listrik)          
            $('#id_kebutuhan_listrik_sehari_hari_konfirmasi').text(respon.data.id_kebutuhan_listrik_sehari_hari)
            $('#id_jumlah_daya_genset_konfirmasi').text(respon.data.id_jumlah_daya_genset)
            $('#id_jumlah_listrik_kebutuhan_dari_pln_konfirmasi').text(respon.data.id_jumlah_listrik_kebutuhan_dari_pln)

            $('#id_air_untuk_rumah_tangga_konfirmasi_konfirmasi').text(respon.data.id_air_untuk_rumah_tangga)
            $('#id_air_untuk_produksi_konfirmasi_konfirmasi').text(respon.data.id_air_untuk_produksi)
            $('#id_air_lainnya_konfirmasi_konfirmasi').text(respon.data.id_air_lainnya)
            var jumlah_kebutuhan_air = parseFloat(respon.data.id_air_untuk_rumah_tangga) + parseFloat(respon.data.id_air_untuk_produksi) + parseFloat(respon.data.id_air_lainnya)
            $('#id_jumlah_kebutuhan_air_konfirmasi_konfirmasi').text(jumlah_kebutuhan_air)

            $('#id_air_dari_pdam_konfirmasi').text(respon.data.id_air_dari_pdam)
            $('#id_air_dari_sumber_konfirmasi').text(respon.data.id_air_dari_sumber)
            $('#id_air_dari_sungai_konfirmasi').text(respon.data.id_air_dari_sungai)
            var jumlah_minimal_kebutuhan_air = parseFloat(respon.data.id_air_dari_pdam) + parseFloat(respon.data.id_air_dari_sumber) + parseFloat(respon.data.id_air_dari_sungai)
            $('#id_jumlah_minimal_kebutuhan_air_konfirmasi').text(jumlah_minimal_kebutuhan_air)

            $('#id_tenaga_kerja_wni_konfirmasi').text(respon.data.id_tenaga_kerja_wni)
            $('#id_tenaga_kerja_wna_konfirmasi').text(respon.data.id_tenaga_kerja_wna)
            $('#id_tenaga_kerja_tetap_konfirmasi').text(respon.data.id_tenaga_kerja_tetap)
            $('#id_tenaga_kerja_tidak_tetap_konfirmasi').text(respon.data.id_tenaga_kerja_tidak_tetap)
            var jumlah_tenaga_kerja = parseFloat(respon.data.id_tenaga_kerja_tetap) + parseFloat(respon.data.id_tenaga_kerja_tidak_tetap)
            $('#id_jumlah_tenaga_kerja_konfirmasi').text(jumlah_tenaga_kerja)

          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}