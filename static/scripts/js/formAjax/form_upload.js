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