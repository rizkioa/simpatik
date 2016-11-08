// +++++++++++++ Ajax Form Upload File Reklame +++++++++++
// 
// 
// 
// ++++++++++++++  upload gambar konstruksi pemasangan reklame ++++++++

var btn_gambar_konstruksi_pemasangan_reklame = $('#btn_gambar_konstruksi_pemasangan_reklame');
var percent_gambar_konstruksi_pemasangan_reklame = $('#percent_gambar_konstruksi_pemasangan_reklame');

$("#form_upload_gambar_konstruksi_pemasangan_reklame").ajaxForm({
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
    	respon = $.parseJSON(response)
    	if(respon.success){
        	toastr["success"](respon.pesan)
        	$('#checkbox_gambar_konstruksi_pemasangan_reklame').prop('checked', true);	
        	var percentVal = '100%';
            percent_gambar_konstruksi_pemasangan_reklame.html(percentVal);												
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

var btn_gambar_foto_lokasi_pemasangan_reklame = $('#btn_gambar_foto_lokasi_pemasangan_reklame');
var percent_gambar_foto_lokasi_pemasangan_reklame = $('#percent_gambar_foto_lokasi_pemasangan_reklame');

$("#form_upload_gambar_foto_lokasi_pemasangan_reklame").ajaxForm({
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
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_gambar_foto_lokasi_pemasangan_reklame').prop('checked', true);   
            var percentVal = '100%';
            percent_gambar_foto_lokasi_pemasangan_reklame.html(percentVal);                                               
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

var btn_gambar_denah_lokasi_pemasangan_reklame = $('#btn_gambar_denah_lokasi_pemasangan_reklame');
var percent_gambar_denah_lokasi_pemasangan_reklame = $('#percent_gambar_denah_lokasi_pemasangan_reklame');

$("#form_upload_gambar_denah_lokasi_pemasangan_reklame").ajaxForm({
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
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_gambar_denah_lokasi_pemasangan_reklame').prop('checked', true);   
            var percentVal = '100%';
            percent_gambar_denah_lokasi_pemasangan_reklame.html(percentVal);                                               
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

var btn_surat_ketetapan_pajak_daerah = $('#btn_surat_ketetapan_pajak_daerah');
var percent_surat_ketetapan_pajak_daerah = $('#percent_surat_ketetapan_pajak_daerah');

$("#form_upload_surat_ketetapan_pajak_daerah").ajaxForm({
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
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_ketetapan_pajak_daerah').prop('checked', true);   
            var percentVal = '100%';
            percent_surat_ketetapan_pajak_daerah.html(percentVal);                                               
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

var btn_surat_setoran_pajak_daerah = $('#btn_surat_setoran_pajak_daerah');
var percent_surat_setoran_pajak_daerah = $('#percent_surat_setoran_pajak_daerah');

$("#form_upload_surat_setoran_pajak_daerah").ajaxForm({
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
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_setoran_pajak_daerah').prop('checked', true);   
            var percentVal = '100%';
            percent_surat_setoran_pajak_daerah.html(percentVal);                                               
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

var btn_rekomendasi_satpol_pp = $('#btn_rekomendasi_satpol_pp');
var percent_rekomendasi_satpol_pp = $('#percent_rekomendasi_satpol_pp');

$("#form_upload_rekomendasi_satpol_pp").ajaxForm({
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
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_rekomendasi_satpol_pp').prop('checked', true);   
            var percentVal = '100%';
            percent_rekomendasi_satpol_pp.html(percentVal);                                               
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

var btn_berita_acara_perusahaan = $('#btn_berita_acara_perusahaan');
var percent_berita_acara_perusahaan = $('#percent_berita_acara_perusahaan');

$("#form_upload_berita_acara_perusahaan").ajaxForm({
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
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_berita_acara_perusahaan').prop('checked', true);   
            var percentVal = '100%';
            percent_berita_acara_perusahaan.html(percentVal);                                               
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

var btn_surat_perjanjian = $('#btn_surat_perjanjian');
var percent_surat_perjanjian = $('#percent_surat_perjanjian');

$("#form_upload_surat_perjanjian").ajaxForm({
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
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_perjanjian').prop('checked', true);   
            var percentVal = '100%';
            percent_surat_perjanjian.html(percentVal);                                               
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

var btn_tambahan = $('#btn_tambahan');
var percent_tambahan = $('#percent_tambahan');

$("#form_upload_berkas_tambahan").ajaxForm({
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
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_perjanjian').prop('checked', true);   
            var percentVal = '100%';
            percent_tambahan.html(percentVal);                                               
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