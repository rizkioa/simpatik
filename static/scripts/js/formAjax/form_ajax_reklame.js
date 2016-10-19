// +++++++++++++ Ajax Form Upload File Reklame +++++++++++
// 
// 
// 
// ++++++++++++++  upload gambar konstruksi pemasangan reklame ++++++++

var btn_berkas_foto = $('#btn_gambar_konstruksi_pemasangan_reklame');
var percent_berkas_foto = $('#percent_gambar_konstruksi_pemasangan_reklame');

$("#form_upload_gambar_konstruksi_pemasangan_reklame").ajaxForm({
	beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_foto.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
    	btn_berkas_foto.hide();
    	percent_berkas_foto.show();
        var percentVal = percentComplete + '%';
        percent_berkas_foto.html(percentVal);
    },
	success: function (response){
    	respon = $.parseJSON(response)
    	if(respon.success){
        	toastr["success"](respon.pesan)
        	$('#checkbox_gambar_konstruksi_pemasangan_reklame').prop('checked', true);	
        	var percentVal = '100%';
            percent_berkas_foto.html(percentVal);												
    	}
    	else{
    		$('#checkbox_gambar_konstruksi_pemasangan_reklame').prop('checked', false);
        	var a = Object.keys(respon);
        	for (var i = 0; i < a.length; i++){
        		var field = a[i].replace("_", " ").capitalize();
        		toastr["error"](field+", "+respon[a[i]][0]['message'])
        		$("#"+a[i]+"").addClass("has-error");
        	btn_berkas_foto.show();
    		percent_berkas_foto.hide();
        	}
    	}
    }
});
// ++++++++++++++ end upload gambar konstruksi pemasangan reklame ++++++++


// ++++++++++++++  upload gambar foto lokasi pemasangan reklame ++++++++

var btn_berkas_foto = $('#btn_gambar_foto_lokasi_pemasangan_reklame');
var percent_berkas_foto = $('#percent_gambar_foto_lokasi_pemasangan_reklame');

$("#form_upload_gambar_foto_lokasi_pemasangan_reklame").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_foto.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_berkas_foto.hide();
        percent_berkas_foto.show();
        var percentVal = percentComplete + '%';
        percent_berkas_foto.html(percentVal);
    },
    success: function (response){
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_gambar_foto_lokasi_pemasangan_reklame').prop('checked', true);   
            var percentVal = '100%';
            percent_berkas_foto.html(percentVal);                                               
        }
        else{
            $('#checkbox_gambar_foto_lokasi_pemasangan_reklame').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_berkas_foto.show();
            percent_berkas_foto.hide();
            }
        }
    }
});
// ++++++++++++++ end upload gambar foto lokasi pemasangan reklame ++++++++


// ++++++++++++++  upload gambar denah lokasi pemasangan reklame ++++++++

var btn_berkas_foto = $('#btn_gambar_denah_lokasi_pemasangan_reklame');
var percent_berkas_foto = $('#percent_gambar_denah_lokasi_pemasangan_reklame');

$("#form_upload_gambar_denah_lokasi_pemasangan_reklame").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_foto.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_berkas_foto.hide();
        percent_berkas_foto.show();
        var percentVal = percentComplete + '%';
        percent_berkas_foto.html(percentVal);
    },
    success: function (response){
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_gambar_denah_lokasi_pemasangan_reklame').prop('checked', true);   
            var percentVal = '100%';
            percent_berkas_foto.html(percentVal);                                               
        }
        else{
            $('#checkbox_gambar_denah_lokasi_pemasangan_reklame').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_berkas_foto.show();
            percent_berkas_foto.hide();
            }
        }
    }
});
// ++++++++++++++ end upload gambar denah lokasi pemasangan reklame ++++++++

// ++++++++++++++  upload surat ketetapan pajak daerah (skpd) ++++++++

var btn_berkas_foto = $('#btn_surat_ketetapan_pajak_daerah');
var percent_berkas_foto = $('#percent_surat_ketetapan_pajak_daerah');

$("#form_upload_surat_ketetapan_pajak_daerah").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_foto.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_berkas_foto.hide();
        percent_berkas_foto.show();
        var percentVal = percentComplete + '%';
        percent_berkas_foto.html(percentVal);
    },
    success: function (response){
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_ketetapan_pajak_daerah').prop('checked', true);   
            var percentVal = '100%';
            percent_berkas_foto.html(percentVal);                                               
        }
        else{
            $('#checkbox_surat_ketetapan_pajak_daerah').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_berkas_foto.show();
            percent_berkas_foto.hide();
            }
        }
    }
});
// ++++++++++++++ end upload surat ketetapan pajak daerah (skpd) ++++++++


// ++++++++++++++  upload surat setoran pajak daerah (sspd) ++++++++

var btn_berkas_foto = $('#btn_surat_setoran_pajak_daerah');
var percent_berkas_foto = $('#percent_surat_setoran_pajak_daerah');

$("#form_upload_surat_setoran_pajak_daerah").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_foto.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_berkas_foto.hide();
        percent_berkas_foto.show();
        var percentVal = percentComplete + '%';
        percent_berkas_foto.html(percentVal);
    },
    success: function (response){
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_setoran_pajak_daerah').prop('checked', true);   
            var percentVal = '100%';
            percent_berkas_foto.html(percentVal);                                               
        }
        else{
            $('#checkbox_surat_setoran_pajak_daerah').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_berkas_foto.show();
            percent_berkas_foto.hide();
            }
        }
    }
});
// ++++++++++++++ end upload surat setoran pajak daerah (sspd) ++++++++


// ++++++++++++++  upload rekomendasi dari kantor SATPOL PP  +++++

var btn_berkas_foto = $('#btn_rekomendasi_satpol_pp');
var percent_berkas_foto = $('#percent_rekomendasi_satpol_pp');

$("#form_upload_rekomendasi_satpol_pp").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_foto.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_berkas_foto.hide();
        percent_berkas_foto.show();
        var percentVal = percentComplete + '%';
        percent_berkas_foto.html(percentVal);
    },
    success: function (response){
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_rekomendasi_satpol_pp').prop('checked', true);   
            var percentVal = '100%';
            percent_berkas_foto.html(percentVal);                                               
        }
        else{
            $('#checkbox_rekomendasi_satpol_pp').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_berkas_foto.show();
            percent_berkas_foto.hide();
            }
        }
    }
});
// ++++++++++++++ end upload rekomendasi dari kantor SATPOL PP ++++++++

// ++++++++++++++  upload berita acara perusahaan  +++++

var btn_berkas_foto = $('#btn_berita_acara_perusahaan');
var percent_berkas_foto = $('#percent_berita_acara_perusahaan');

$("#form_upload_berita_acara_perusahaan").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_foto.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_berkas_foto.hide();
        percent_berkas_foto.show();
        var percentVal = percentComplete + '%';
        percent_berkas_foto.html(percentVal);
    },
    success: function (response){
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_berita_acara_perusahaan').prop('checked', true);   
            var percentVal = '100%';
            percent_berkas_foto.html(percentVal);                                               
        }
        else{
            $('#checkbox_berita_acara_perusahaan').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_berkas_foto.show();
            percent_berkas_foto.hide();
            }
        }
    }
});
// ++++++++++++++ end upload berita acara perusahaan ++++++++


// ++++++++++++++ upload surat perjanjian +++++

var btn_berkas_foto = $('#btn_surat_perjanjian');
var percent_berkas_foto = $('#percent_surat_perjanjian');

$("#form_upload_surat_perjanjian").ajaxForm({
    beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_foto.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
        btn_berkas_foto.hide();
        percent_berkas_foto.show();
        var percentVal = percentComplete + '%';
        percent_berkas_foto.html(percentVal);
    },
    success: function (response){
        respon = $.parseJSON(response)
        if(respon.success){
            toastr["success"](respon.pesan)
            $('#checkbox_surat_perjanjian').prop('checked', true);   
            var percentVal = '100%';
            percent_berkas_foto.html(percentVal);                                               
        }
        else{
            $('#checkbox_surat_perjanjian').prop('checked', false);
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
                var field = a[i].replace("_", " ").capitalize();
                toastr["error"](field+", "+respon[a[i]][0]['message'])
                $("#"+a[i]+"").addClass("has-error");
            btn_berkas_foto.show();
            percent_berkas_foto.hide();
            }
        }
    }
});
// ++++++++++++++ end upload surat perjanjian++++++++