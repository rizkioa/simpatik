// +++++++++++++ Ajax Form Upload File Reklame +++++++++++
// 
// 
// 
// ++++++++++++++  upload gambar konstruksi pemasangan reklame ++++++++

var btn_gambar_konstruksi_pemasangan_reklame = $('#btn-gambar_konstruksi_pemasangan_reklame');
var percent_gambar_konstruksi_pemasangan_reklame = $('#percent-gambar_konstruksi_pemasangan_reklame');

$("#form-upload_gambar_konstruksi_pemasangan_reklame").ajaxForm({
	beforeSend: function() {
        var percentVal = '0%';
        percent_gambar_konstruksi_pemasangan_reklame.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
    	btn_gambar_konstruksi_pemasangan_reklame.hide();
    	percent_gambar_konstruksi_pemasangan_reklame.show();
        var percentVal = percentComplete + '%';
        percent_gambar_konstruksi_pemasangan_reklame.html(percentVal);
    },
	success: function (response){
        var elem_ = $("#form-upload_gambar_konstruksi_pemasangan_reklame")[0].id
        var split_ = elem_.split('-')[1]
    	respon = $.parseJSON(response)
    	if(respon.success){
        	toastr["success"](respon.pesan)
        	$('#checkbox_gambar_konstruksi_pemasangan_reklame').prop('checked', true);	
        	var percentVal = '100%';
            $('#percent-'+split_).html(percentVal);
            if ($.cookie('id_pengajuan') !== undefined){
              load_berkas($.cookie('id_pengajuan'))
            }  										
    	}
    	else{
    		$('#checkbox_gambar_konstruksi_pemasangan_reklame').prop('checked', false);
        	var a = Object.keys(respon);
        	for (var i = 0; i < a.length; i++){
        		var field = a[i].replace("_", " ").capitalize();
        		toastr["error"](field+", "+respon[a[i]][0]['message'])
        		$("#"+a[i]+"").addClass("has-error");
        	btn_gambar_konstruksi_pemasangan_reklame.show();
    		percent_gambar_konstruksi_pemasangan_reklame.hide();
        	}
    	}
    }
});
// ++++++++++++++ end upload gambar konstruksi pemasangan reklame ++++++++


// ++++++++++++++  upload gambar foto lokasi pemasangan reklame ++++++++

var btn_gambar_foto_lokasi_pemasangan_reklame = $('#btn-gambar_foto_lokasi_pemasangan_reklame');
var percent_gambar_foto_lokasi_pemasangan_reklame = $('#percent-gambar_foto_lokasi_pemasangan_reklame');

$("#form-upload_gambar_foto_lokasi_pemasangan_reklame").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_gambar_foto_lokasi_pemasangan_reklame.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_gambar_foto_lokasi_pemasangan_reklame.hide();
        percent_gambar_foto_lokasi_pemasangan_reklame.show();
        var percentVal = percentComplete + '%';
        percent_gambar_foto_lokasi_pemasangan_reklame.html(percentVal);
    },
    success: function (response){
        var elem_ = $("#form-upload_gambar_foto_lokasi_pemasangan_reklame")[0].id
        var split_ = elem_.split('-')[1]
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_gambar_foto_lokasi_pemasangan_reklame').prop('checked', true);   
            var percentVal = '100%';
            $('#percent-'+split_).html(percentVal);
            if ($.cookie('id_pengajuan') !== undefined){
              load_berkas($.cookie('id_pengajuan'))
            }                                                
        }
        else{
            $('#checkbox_gambar_foto_lokasi_pemasangan_reklame').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_gambar_foto_lokasi_pemasangan_reklame.show();
            percent_gambar_foto_lokasi_pemasangan_reklame.hide();
            }
        }
    }
});
// ++++++++++++++ end upload gambar foto lokasi pemasangan reklame ++++++++


// ++++++++++++++  upload gambar denah lokasi pemasangan reklame ++++++++

var btn_gambar_denah_lokasi_pemasangan_reklame = $('#btn-gambar_denah_lokasi_pemasangan_reklame');
var percent_gambar_denah_lokasi_pemasangan_reklame = $('#percent-gambar_denah_lokasi_pemasangan_reklame');

$("#form-upload_gambar_denah_lokasi_pemasangan_reklame").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_gambar_denah_lokasi_pemasangan_reklame.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_gambar_denah_lokasi_pemasangan_reklame.hide();
        percent_gambar_denah_lokasi_pemasangan_reklame.show();
        var percentVal = percentComplete + '%';
        percent_gambar_denah_lokasi_pemasangan_reklame.html(percentVal);
    },
    success: function (response){
        var elem_ = $("#form-upload_gambar_denah_lokasi_pemasangan_reklame")[0].id
        var split_ = elem_.split('-')[1]
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_gambar_denah_lokasi_pemasangan_reklame').prop('checked', true);   
            var percentVal = '100%';
            $('#percent-'+split_).html(percentVal);
            if ($.cookie('id_pengajuan') !== undefined){
              load_berkas($.cookie('id_pengajuan'))
            }                                                  
        }
        else{
            $('#checkbox_gambar_denah_lokasi_pemasangan_reklame').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_gambar_denah_lokasi_pemasangan_reklame.show();
            percent_gambar_denah_lokasi_pemasangan_reklame.hide();
            }
        }
    }
});
// ++++++++++++++ end upload gambar denah lokasi pemasangan reklame ++++++++

// ++++++++++++++  upload surat ketetapan pajak daerah (skpd) ++++++++

var btn_surat_ketetapan_pajak_daerah = $('#btn-surat_ketetapan_pajak_daerah');
var percent_surat_ketetapan_pajak_daerah = $('#percent-surat_ketetapan_pajak_daerah');

$("#form-upload_surat_ketetapan_pajak_daerah").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_surat_ketetapan_pajak_daerah.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_surat_ketetapan_pajak_daerah.hide();
        percent_surat_ketetapan_pajak_daerah.show();
        var percentVal = percentComplete + '%';
        percent_surat_ketetapan_pajak_daerah.html(percentVal);
    },
    success: function (response){
        var elem_ = $("#form-upload_surat_ketetapan_pajak_daerah")[0].id
        var split_ = elem_.split('-')[1]
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_ketetapan_pajak_daerah').prop('checked', true);   
            var percentVal = '100%';
            $('#percent-'+split_).html(percentVal);
            if ($.cookie('id_pengajuan') !== undefined){
              load_berkas($.cookie('id_pengajuan'))
            }                                                 
        }
        else{
            $('#checkbox_surat_ketetapan_pajak_daerah').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_surat_ketetapan_pajak_daerah.show();
            percent_surat_ketetapan_pajak_daerah.hide();
            }
        }
    }
});
// ++++++++++++++ end upload surat ketetapan pajak daerah (skpd) ++++++++


// ++++++++++++++  upload surat setoran pajak daerah (sspd) ++++++++

var btn_surat_setoran_pajak_daerah = $('#btn-surat_setoran_pajak_daerah');
var percent_surat_setoran_pajak_daerah = $('#percent-surat_setoran_pajak_daerah');

$("#form-upload_surat_setoran_pajak_daerah").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_surat_setoran_pajak_daerah.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_surat_setoran_pajak_daerah.hide();
        percent_surat_setoran_pajak_daerah.show();
        var percentVal = percentComplete + '%';
        percent_surat_setoran_pajak_daerah.html(percentVal);
    },
    success: function (response){
        var elem_ = $("#form-upload_surat_setoran_pajak_daerah")[0].id
        var split_ = elem_.split('-')[1]
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_setoran_pajak_daerah').prop('checked', true);   
            var percentVal = '100%';
            $('#percent-'+split_).html(percentVal);
            if ($.cookie('id_pengajuan') !== undefined){
              load_berkas($.cookie('id_pengajuan'))
            }                                             
        }
        else{
            $('#checkbox_surat_setoran_pajak_daerah').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_surat_setoran_pajak_daerah.show();
            percent_surat_setoran_pajak_daerah.hide();
            }
        }
    }
});
// ++++++++++++++ end upload surat setoran pajak daerah (sspd) ++++++++


// ++++++++++++++  upload rekomendasi dari kantor SATPOL PP  +++++

var btn_rekomendasi_satpol_pp = $('#btn-rekomendasi_satpol_pp');
var percent_rekomendasi_satpol_pp = $('#percent-rekomendasi_satpol_pp');

$("#form-upload_rekomendasi_satpol_pp").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_rekomendasi_satpol_pp.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_rekomendasi_satpol_pp.hide();
        percent_rekomendasi_satpol_pp.show();
        var percentVal = percentComplete + '%';
        percent_rekomendasi_satpol_pp.html(percentVal);
    },
    success: function (response){
        var elem_ = $("#form-upload_rekomendasi_satpol_pp")[0].id
        var split_ = elem_.split('-')[1]
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_rekomendasi_satpol_pp').prop('checked', true);   
            var percentVal = '100%';
            $('#percent-'+split_).html(percentVal);
            if ($.cookie('id_pengajuan') !== undefined){
              load_berkas($.cookie('id_pengajuan'))
            }                                              
        }
        else{
            $('#checkbox_rekomendasi_satpol_pp').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_rekomendasi_satpol_pp.show();
            percent_rekomendasi_satpol_pp.hide();
            }
        }
    }
});
// ++++++++++++++ end upload rekomendasi dari kantor SATPOL PP ++++++++

// ++++++++++++++  upload berita acara perusahaan  +++++

var btn_berita_acara_perusahaan = $('#btn-berita_acara_perusahaan');
var percent_berita_acara_perusahaan = $('#percent-berita_acara_perusahaan');

$("#form-upload_berita_acara_perusahaan").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_berita_acara_perusahaan.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_berita_acara_perusahaan.hide();
        percent_berita_acara_perusahaan.show();
        var percentVal = percentComplete + '%';
        percent_berita_acara_perusahaan.html(percentVal);
    },
    success: function (response){
        var elem_ = $("#form-upload_berita_acara_perusahaan")[0].id
        var split_ = elem_.split('-')[1]
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_berita_acara_perusahaan').prop('checked', true);   
            var percentVal = '100%';
            $('#percent-'+split_).html(percentVal);
            if ($.cookie('id_pengajuan') !== undefined){
              load_berkas($.cookie('id_pengajuan'))
            }                                           
        }
        else{
            $('#checkbox_berita_acara_perusahaan').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_berita_acara_perusahaan.show();
            percent_berita_acara_perusahaan.hide();
            }
        }
    }
});
// ++++++++++++++ end upload berita acara perusahaan ++++++++


// ++++++++++++++ upload surat perjanjian +++++

var btn_surat_perjanjian = $('#btn-surat_perjanjian');
var percent_surat_perjanjian = $('#percent-surat_perjanjian');

$("#form-upload_surat_perjanjian").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_surat_perjanjian.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_surat_perjanjian.hide();
        percent_surat_perjanjian.show();
        var percentVal = percentComplete + '%';
        percent_surat_perjanjian.html(percentVal);
    },
    success: function (response){
        var elem_ = $("#form-upload_surat_perjanjian")[0].id
        var split_ = elem_.split('-')[1]
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_perjanjian').prop('checked', true);   
            var percentVal = '100%';
            $('#percent-'+split_).html(percentVal);
            if ($.cookie('id_pengajuan') !== undefined){
              load_berkas($.cookie('id_pengajuan'))
            }                                               
        }
        else{
            $('#checkbox_surat_perjanjian').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_surat_perjanjian    .show();
            percent_surat_perjanjian.hide();
            }
        }
    }
});
// ++++++++++++++ end upload surat perjanjian++++++++

// ++++++++++++++ upload surat perjanjian +++++

var btn_tambahan = $('#btn-tambahan');
var percent_tambahan = $('#percent-tambahan');

$("#form-upload_berkas_tambahan").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_tambahan.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_tambahan.hide();
        percent_tambahan.show();
        var percentVal = percentComplete + '%';
        percent_tambahan.html(percentVal);
    },
    success: function (response){
        var elem_ = $("#form-upload_berkas_tambahan")[0].id
        var split_ = elem_.split('-')[1]
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_perjanjian').prop('checked', true);   
            var percentVal = '100%';
            $('#percent-'+split_).html(percentVal);
            if ($.cookie('id_pengajuan') !== undefined){
              load_berkas($.cookie('id_pengajuan'))
            }                                               
        }
        else{
            $('#checkbox_surat_perjanjian').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_tambahan.show();
            percent_tambahan.hide();
            }
        }
    }
});
// ++++++++++++++ end upload surat perjanjian++++++++

function load_berkas(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ajax-load-berkas-reklame/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          len = respon.berkas.length
          for (var i = 0; i < len; i++) {
            // console.log(respon.berkas[i])
            // console.log(respon.elemen[i])
            // console.log(respon.id_berkas[i])
            url = '<a id="btn-load-'+respon.elemen[i]+'" class="btn btn-success btn-sm" data-toggle="popover" data-trigger="hover" data-container="body" data-placement="bottom" href="'+respon.berkas[i]+'" target="blank_"> <i class="fa fa-check"></i> '+respon.nm_berkas[i]+' </a> <a class="btn btn-danger btn-sm" onclick="delete_berkas_upload('+respon.id_berkas[i]+',\''+respon.elemen[i]+'\', '+id_pengajuan+');return false;" > <i class="fa fa-trash"></i> Hapus</a>'
            // console.log(url)
            $('#load-'+respon.elemen[i]).html(url)
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

function delete_berkas_upload(id, elemen, id_pengajuan){
  // $('#field-'+elemen).show()
  $(".tab-content").mLoading();
  $.ajax({
    url: __base_url__+'/ajax-delete-berkas-reklame-upload/'+id,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          toastr["success"](respon.pesan)
            $('#field-'+elemen).show()
            $('#load-'+elemen).html('')
            $('#checkbox-'+elemen).prop('checked', false); 
            $('#percent-'+elemen).hide()
            $('#btn-'+elemen).show()
            $('#field-'+elemen).find('.id_berkas').filestyle("clear")
          // load_berkas(id_perusahaan)
        }
      },
      error: function(response){
      toast_server_error()
    }
  })
  $(".tab-content").mLoading('hide');
}

