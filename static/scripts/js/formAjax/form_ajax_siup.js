
	//berkas foto pemohon

	// var btn_berkas_foto = $('#btn_berkas_foto');
	// var percent_berkas_foto = $('#percent_berkas_foto');

	// $("#form_berkas_foto").ajaxForm({
	// 	beforeSend: function() {
 //        var percentVal = '0%';
 //        percent_berkas_foto.html(percentVal);
 //    },
 //    uploadProgress: function(event, position, total, percentComplete) {
 //    	btn_berkas_foto.hide();
 //    	percent_berkas_foto.show();
 //        var percentVal = percentComplete + '%';
 //        percent_berkas_foto.html(percentVal);
 //    },
	// 	success: function (response){
	// 	respon = $.parseJSON(response)
	// 	if(respon.success){
 //        	toastr["success"](respon.pesan)
 //        	$('#checkbox_berkas_foto').prop('checked', true);	
 //        	var percentVal = '100%';
	//         percent_berkas_foto.html(percentVal);												
	// 	}
	// 	else{
	// 		$('#checkbox_berkas_foto').prop('checked', false);
 //        	var a = Object.keys(respon);
 //        	for (var i = 0; i < a.length; i++){
 //        		var field = a[i].replace("_", " ").capitalize();
 //        		toastr["error"](field+", "+respon[a[i]][0]['message'])
 //        		$("#"+a[i]+"").addClass("has-error");
 //        	btn_berkas_foto.show();
 //    		percent_berkas_foto.hide();
 //        	}
	// 	}
	// }
	// });

	// // berkas ktp atau paspor pemohon

	// var btn_berkas_ktp = $('#btn_berkas_ktp');
	// var percent_berkas_ktp = $('#percent_berkas_ktp');

	// $("#form_berkas_ktp").ajaxForm({
	// 	beforeSend: function() {
 //        var percentVal = '0%';
 //        percent_berkas_ktp.html(percentVal);
 //    },
 //    uploadProgress: function(event, position, total, percentComplete) {
 //    	btn_berkas_ktp.hide();
 //    	percent_berkas_ktp.show();
 //        var percentVal = percentComplete + '%';
 //        percent_berkas_ktp.html(percentVal);
 //    },
	// 	success: function (response){
	// 	respon = $.parseJSON(response)
	// 	if(respon.success){
 //        	toastr["success"](respon.pesan)
	// 		$('#checkbox_berkas_ktp').prop('checked', true);
 //        	var percentVal = '100%';
	//         percent_berkas_ktp.html(percentVal);												
	// 	}
	// 	else{
	// 		$('#checkbox_berkas_ktp').prop('checked', false);
 //        	var a = Object.keys(respon);
 //        	for (var i = 0; i < a.length; i++){
 //        		var field = a[i].replace("_", " ").capitalize();
 //        		toastr["error"](field+", "+respon[a[i]][0]['message'])
 //        		$("#"+a[i]+"").addClass("has-error");
 //        	btn_berkas_ktp.show();
 //    		percent_berkas_ktp.hide();
 //        	}
	// 	}
	// }
	// });

	// // berkas npwp pribadi

	// var btn_berkas_npwp_pribadi = $('#btn_berkas_npwp_pribadi');
	// var percent_berkas_npwp_pribadi = $('#percent_berkas_npwp_pribadi');

	// $("#form_berkas_npwp_pribadi").ajaxForm({
	// 	beforeSend: function() {
 //        var percentVal = '0%';
 //        percent_berkas_npwp_pribadi.html(percentVal);
 //    },
 //    uploadProgress: function(event, position, total, percentComplete) {
 //    	btn_berkas_npwp_pribadi.hide();
 //    	percent_berkas_npwp_pribadi.show();
 //        var percentVal = percentComplete + '%';
 //        percent_berkas_npwp_pribadi.html(percentVal);
 //    },
	// 	success: function (response){
	// 	respon = $.parseJSON(response)
	// 	if(respon.success){
 //        	toastr["success"](respon.pesan)
	// 		$('#checkbox_berkas_npwp_pribadi').prop('checked', true);
 //        	var percentVal = '100%';
	//         percent_berkas_npwp_pribadi.html(percentVal);												
	// 	}
	// 	else{
	// 		$('#checkbox_berkas_npwp_pribadi').prop('checked', false);
 //        	var a = Object.keys(respon);
 //        	for (var i = 0; i < a.length; i++){
 //        		var field = a[i].replace("_", " ").capitalize();
 //        		toastr["error"](field+", "+respon[a[i]][0]['message'])
 //        		$("#"+a[i]+"").addClass("has-error");
 //        	btn_berkas_npwp_pribadi.show();
 //    		percent_berkas_npwp_pribadi.hide();
 //        	}
	// 	}
	// }
	// });

	// // berkas npwp perusahaan

	// var percent_berkas_npwp_perusahaan = $('#percent_berkas_npwp_perusahaan');
	// var btn_berkas_npwp_perusahaan = $('#button_berkas_npwp_perusahaan');
	// $("#form_berkas_npwp_perusahaan").ajaxForm({	  		

	// 	beforeSend: function() {
 //        var percentVal = '0%';
 //        percent_berkas_npwp_perusahaan.html(percentVal);
 //    },
 //    uploadProgress: function(event, position, total, percentComplete) {
 //    	btn_berkas_npwp_perusahaan.hide();
 //    	percent_berkas_npwp_perusahaan.show();
 //        var percentVal = percentComplete + '%';
 //        percent_berkas_npwp_perusahaan.html(percentVal);
 //    },
	// 	success: function (response){
	// 	respon = $.parseJSON(response)
	// 	if(respon.success){
 //        	toastr["success"](respon.pesan)
	// 		$('#checkbox_berkas_npwp_perusahaan').prop('checked', true);
 //        	var percentVal = '100%';
	//         percent_berkas_npwp_perusahaan.html(percentVal);												
	// 	}
	// 	else{
	// 		$('#checkbox_berkas_npwp_perusahaan').prop('checked', false);
 //        	var a = Object.keys(respon);
 //        	for (var i = 0; i < a.length; i++){
 //        		var field = a[i].replace("_", " ").capitalize();
 //        		toastr["error"](field+", "+respon[a[i]][0]['message'])
 //        		$("#"+a[i]+"").addClass("has-error");
 //        	btn_berkas_npwp_perusahaan.show();
 //    		percent_berkas_npwp_perusahaan.hide();
 //        	}
	// 	}
	// }
	// });

	// // berkas akta pendirian

	// var btn_berkas_akta_pendirian = $('#btn_berkas_akta_pendirian');
	// var percent_berkas_akta_pendirian = $('#percent_berkas_akta_pendirian');

	// $("#form_berkas_akta_pendirian").ajaxForm({
	// 	beforeSend: function() {
 //        var percentVal = '0%';
 //        percent_berkas_akta_pendirian.html(percentVal);
 //    },
 //    uploadProgress: function(event, position, total, percentComplete) {
 //    	btn_berkas_akta_pendirian.hide();
 //    	percent_berkas_akta_pendirian.show();
 //        var percentVal = percentComplete + '%';
 //        percent_berkas_akta_pendirian.html(percentVal);
 //    },
	// 	success: function (response){
	// 	respon = $.parseJSON(response)
	// 	if(respon.success){
 //        	toastr["success"](respon.pesan)
	// 		$('#checkbox_berkas_akta_pendirian').prop('checked', true);
 //        	var percentVal = '100%';
	//         percent_berkas_akta_pendirian.html(percentVal);												
	// 	}
	// 	else{
	// 		$('#checkbox_berkas_akta_pendirian').prop('checked', false);
 //        	var a = Object.keys(respon);
 //        	for (var i = 0; i < a.length; i++){
 //        		var field = a[i].replace("_", " ").capitalize();
 //        		toastr["error"](field+", "+respon[a[i]][0]['message'])
 //        		$("#"+a[i]+"").addClass("has-error");
 //        	btn_berkas_akta_pendirian.show();
 //    		percent_berkas_akta_pendirian.hide();
 //        	}
	// 	}
	// }
	// });

	// // berkas akta perubahan
	
	// var btn_berkas_akta_perubahan = $('#btn_berkas_akta_perubahan');
	// var percent_berkas_akta_perubahan = $('#percent_berkas_akta_perubahan');

	// $("#form_berkas_akta_perubahan").ajaxForm({
	// 	beforeSend: function() {
 //        var percentVal = '0%';
 //        percent_berkas_akta_perubahan.html(percentVal);
 //    },
 //    uploadProgress: function(event, position, total, percentComplete) {
 //    	btn_berkas_akta_perubahan.hide();
 //    	percent_berkas_akta_perubahan.show();
 //        var percentVal = percentComplete + '%';
 //        percent_berkas_akta_perubahan.html(percentVal);
 //    },
	// 	success: function (response){
	// 	respon = $.parseJSON(response)
	// 	if(respon.success){
 //        	toastr["success"](respon.pesan)
	// 		$('#checkbox_berkas_akta_pembaruan').prop('checked', true);
 //        	var percentVal = '100%';
	//         percent_berkas_akta_perubahan.html(percentVal);												
	// 	}
	// 	else{
	// 		$('#checkbox_berkas_akta_pembaruan').prop('checked', false);
	// 		btn_berkas_akta_perubahan.show();
 //    		percent_berkas_akta_perubahan.hide();
 //        	var a = Object.keys(respon);
 //        	for (var i = 0; i < a.length; i++){
 //        		var field = a[i].replace("_", " ").capitalize();
 //        		toastr["error"](field+", "+respon[a[i]][0]['message'])
 //        		$("#"+a[i]+"").addClass("has-error");
 //        	}
	// 	}
	// }
	// });

	// // berkas pendukung
	
	// var btn_berkas_pendukung = $('#btn_berkas_pendukung');
	// var percent_berkas_pendukung = $('#percent_berkas_pendukung');

	// $("#form_berkas_pendukung").ajaxForm({

	// 	beforeSend: function() {
 //        var percentVal = '0%';
 //        percent_berkas_pendukung.html(percentVal);
 //    },
 //    uploadProgress: function(event, position, total, percentComplete) {
 //    	btn_berkas_pendukung.hide();
 //    	percent_berkas_pendukung.show();
 //        var percentVal = percentComplete + '%';
 //        percent_berkas_pendukung.html(percentVal);
 //    },
	// 	success: function (response){
	// 	respon = $.parseJSON(response)
	// 	if(respon.success){
 //        	toastr["success"](respon.pesan)
	// 		$('#checkbox_berkas_pendukung').prop('checked', true);
 //        	for (var i = 0; i < respon.data.length; i++){
 //        		var key = Object.keys(respon.data[i]); // Mencari key json
 //        		// console.log(key[0]);
 //        		if (key[0]= "status_upload") {
 //        			$("#npwp_perusahaan").hide(1000)
 //        		}else{
 //            		var val = respon.data[i][key[0]] // mencari value json
 //            		// console.log(key[0]+"_konfirmasi");
 //            		var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi

 //            		$(id).text(val);
 //            	}
 //        	}	
 //        	var percentVal = '100%';
	//         percent_berkas_pendukung.html(percentVal);												
	// 	}
	// 	else{
	// 		$('#checkbox_berkas_pendukung').prop('checked', false);
 //        	var a = Object.keys(respon);
 //        	for (var i = 0; i < a.length; i++){
 //        		var field = a[i].replace("_", " ").capitalize();
 //        		toastr["error"](field+", "+respon[a[i]][0]['message'])
 //        		$("#"+a[i]+"").addClass("has-error");
 //        	btn_berkas_pendukung.show();
 //    		percent_berkas_pendukung.hide();
 //        	}
	// 	}
	// }
	// });

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
          url: __base_url__+'/ajax-load-berkas-siup/'+id_pengajuan,
          success: function (response){
            respon = $.parseJSON(response)
            if (respon.success) {
              len = respon.berkas.length
              for (var i = 0; i < len; i++) {
                // console.log(respon.berkas[i])
                // console.log(respon.elemen[i])
                // console.log(respon.id_berkas[i])
                url = '<a style="min-width: 742px;text-align: left;" id="btn-load-'+respon.elemen[i]+'" class="btn btn-success btn-sm" data-toggle="popover" data-trigger="hover" data-container="body" data-placement="bottom" href="'+respon.berkas[i]+'" target="blank_"> <i class="fa fa-check"></i> '+respon.nm_berkas[i]+' </a> <a class="btn btn-danger btn-sm" onclick="delete_berkas_upload('+respon.id_berkas[i]+',\''+respon.elemen[i]+'\');return false;" > <i class="fa fa-trash"></i> Hapus</a>'
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

    function delete_berkas_upload(id, elemen){
      // $('#field-'+elemen).show()
      $(".tab-content").mLoading();
      
      $.ajax({
        url: url = __base_url__+'/ajax-delete-berkas-upload/'+id+'/'+elemen,
          success: function (response){
            respon = $.parseJSON(response)
            if (respon.success) {
              toastr["success"](respon.pesan)
              $('#form-'+elemen)[0].reset() 
              $('#percent-'+elemen).hide()
              $('#btn-'+elemen).show()
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
    // **** END *****