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
