
	//berkas foto pemohon

	var btn_berkas_foto = $('#btn_berkas_foto');
	var percent_berkas_foto = $('#percent_berkas_foto');

	$("#form_berkas_foto").ajaxForm({
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
        	$('#checkbox_berkas_foto').prop('checked', true);
        	// $.cookie("keys", "value"); set cookie
        	// for (var i = 0; i < respon.data.length; i++){
        	// 	var key = Object.keys(respon.data[i]); // Mencari key json
        	// 	// console.log(key[0]);
        	// 	if (key[0]= "status_upload") {
        	// 		$("#npwp_perusahaan").hide(1000)
        	// 	}else{
            // 		var val = respon.data[i][key[0]] // mencari value json
            // 		// console.log(key[0]+"_konfirmasi");
            // 		var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi

            // 		$(id).text(val);
            // 	}
        	// }	
        	var percentVal = '100%';
	        percent_berkas_foto.html(percentVal);												
		}
		else{
			$('#checkbox_berkas_foto').prop('checked', false);
			// console.log(respon);
        	// console.log(typeof respon);
        	var a = Object.keys(respon);
        	// console.log(respon['nama_lengkap'][0]['message']);
        	// console.log(a.length);
        	for (var i = 0; i < a.length; i++){
        		// console.log(a[i]);
        		// console.log(respon[a[i]]);
        		var field = a[i].replace("_", " ").capitalize();
        		toastr["error"](field+", "+respon[a[i]][0]['message'])
        		$("#"+a[i]+"").addClass("has-error");
        		// console.log($("#"+a[i]+"").addClass("parsley-error"));
        	btn_berkas_foto.show();
    		percent_berkas_foto.hide();
        	}
		}
	}
	});

	// berkas ktp atau paspor pemohon

	var btn_berkas_ktp = $('#btn_berkas_ktp');
	var percent_berkas_ktp = $('#percent_berkas_ktp');

	$("#form_berkas_ktp").ajaxForm({
		beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_ktp.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
    	btn_berkas_ktp.hide();
    	percent_berkas_ktp.show();
        var percentVal = percentComplete + '%';
        percent_berkas_ktp.html(percentVal);
    },
		success: function (response){
		respon = $.parseJSON(response)
		if(respon.success){
        	toastr["success"](respon.pesan)
			$('#checkbox_berkas_ktp').prop('checked', true);
        	// $.cookie("keys", "value"); set cookie
        	// for (var i = 0; i < respon.data.length; i++){
        	// 	var key = Object.keys(respon.data[i]); // Mencari key json
        	// 	// console.log(key[0]);
        	// 	if (key[0]= "status_upload") {
        	// 		$("#npwp_perusahaan").hide(1000)
        	// 	}else{
            // 		var val = respon.data[i][key[0]] // mencari value json
            // 		// console.log(key[0]+"_konfirmasi");
            // 		var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi

            // 		$(id).text(val);
            // 	}
        	// }	
        	var percentVal = '100%';
	        percent_berkas_ktp.html(percentVal);												
		}
		else{
			$('#checkbox_berkas_ktp').prop('checked', false);
			// console.log(respon);
        	// console.log(typeof respon);
        	var a = Object.keys(respon);
        	// console.log(respon['nama_lengkap'][0]['message']);
        	// console.log(a.length);
        	for (var i = 0; i < a.length; i++){
        		// console.log(a[i]);
        		// console.log(respon[a[i]]);
        		var field = a[i].replace("_", " ").capitalize();
        		toastr["error"](field+", "+respon[a[i]][0]['message'])
        		$("#"+a[i]+"").addClass("has-error");
        		// console.log($("#"+a[i]+"").addClass("parsley-error"));
        	btn_berkas_ktp.show();
    		percent_berkas_ktp.hide();
        	}
		}
	}
	});

	// berkas npwp pribadi

	var btn_berkas_npwp_pribadi = $('#btn_berkas_npwp_pribadi');
	var percent_berkas_npwp_pribadi = $('#percent_berkas_npwp_pribadi');

	$("#form_berkas_npwp_pribadi").ajaxForm({
		beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_npwp_pribadi.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
    	btn_berkas_npwp_pribadi.hide();
    	percent_berkas_npwp_pribadi.show();
        var percentVal = percentComplete + '%';
        percent_berkas_npwp_pribadi.html(percentVal);
    },
		success: function (response){
		respon = $.parseJSON(response)
		if(respon.success){
        	toastr["success"](respon.pesan)
			$('#checkbox_berkas_npwp_pribadi').prop('checked', true);

        	// $.cookie("keys", "value"); set cookie
        	// for (var i = 0; i < respon.data.length; i++){
        	// 	var key = Object.keys(respon.data[i]); // Mencari key json
        	// 	// console.log(key[0]);
        	// 	if (key[0]= "status_upload") {
        	// 		$("#npwp_perusahaan").hide(1000)
        	// 	}else{
            // 		var val = respon.data[i][key[0]] // mencari value json
            // 		// console.log(key[0]+"_konfirmasi");
            // 		var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi

            // 		$(id).text(val);
            // 	}
        	// }	
        	var percentVal = '100%';
	        percent_berkas_npwp_pribadi.html(percentVal);												
		}
		else{
			$('#checkbox_berkas_npwp_pribadi').prop('checked', false);
			// console.log(respon);
        	// console.log(typeof respon);
        	var a = Object.keys(respon);
        	// console.log(respon['nama_lengkap'][0]['message']);
        	// console.log(a.length);
        	for (var i = 0; i < a.length; i++){
        		// console.log(a[i]);
        		// console.log(respon[a[i]]);
        		var field = a[i].replace("_", " ").capitalize();
        		toastr["error"](field+", "+respon[a[i]][0]['message'])
        		$("#"+a[i]+"").addClass("has-error");
        		// console.log($("#"+a[i]+"").addClass("parsley-error"));
        	btn_berkas_npwp_pribadi.show();
    		percent_berkas_npwp_pribadi.hide();
        	}
		}
	}
	});

	// berkas npwp perusahaan

	var percent_berkas_npwp_perusahaan = $('#percent_berkas_npwp_perusahaan');
	var btn_berkas_npwp_perusahaan = $('#button_berkas_npwp_perusahaan');
	$("#form_berkas_npwp_perusahaan").ajaxForm({	  		

		beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_npwp_perusahaan.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
    	btn_berkas_npwp_perusahaan.hide();
    	percent_berkas_npwp_perusahaan.show();
        var percentVal = percentComplete + '%';
        percent_berkas_npwp_perusahaan.html(percentVal);
    },
		success: function (response){
		respon = $.parseJSON(response)
		if(respon.success){
        	toastr["success"](respon.pesan)
			$('#checkbox_berkas_npwp_perusahaan').prop('checked', true);
        	// $.cookie("keys", "value"); set cookie
        	// for (var i = 0; i < respon.data.length; i++){
        	// 	var key = Object.keys(respon.data[i]); // Mencari key json
        	// 	// console.log(key[0]);
        	// 	if (key[0]= "status_upload") {
        	// 		$("#npwp_perusahaan").hide(1000)
        	// 	}else{
            // 		var val = respon.data[i][key[0]] // mencari value json
            // 		// console.log(key[0]+"_konfirmasi");
            // 		var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi

            // 		$(id).text(val);
            // 	}
        	// }	
        	var percentVal = '100%';
	        percent_berkas_npwp_perusahaan.html(percentVal);												
		}
		else{
			$('#checkbox_berkas_npwp_perusahaan').prop('checked', false);
			// console.log(respon);
        	// console.log(typeof respon);
        	var a = Object.keys(respon);
        	// console.log(respon['nama_lengkap'][0]['message']);
        	// console.log(a.length);
        	for (var i = 0; i < a.length; i++){
        		// console.log(a[i]);
        		// console.log(respon[a[i]]);
        		var field = a[i].replace("_", " ").capitalize();
        		toastr["error"](field+", "+respon[a[i]][0]['message'])
        		$("#"+a[i]+"").addClass("has-error");
        		// console.log($("#"+a[i]+"").addClass("parsley-error"));
        	btn_berkas_npwp_perusahaan.show();
    		percent_berkas_npwp_perusahaan.hide();
        	}
		}
	}
	});

	// berkas akta pendirian

	var btn_berkas_akta_pendirian = $('#btn_berkas_akta_pendirian');
	var percent_berkas_akta_pendirian = $('#percent_berkas_akta_pendirian');

	$("#form_berkas_akta_pendirian").ajaxForm({
		beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_akta_pendirian.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
    	btn_berkas_akta_pendirian.hide();
    	percent_berkas_akta_pendirian.show();
        var percentVal = percentComplete + '%';
        percent_berkas_akta_pendirian.html(percentVal);
    },
		success: function (response){
		respon = $.parseJSON(response)
		if(respon.success){
        	toastr["success"](respon.pesan)
			$('#checkbox_berkas_akta_pendirian').prop('checked', true);
        	// $.cookie("keys", "value"); set cookie
        	// for (var i = 0; i < respon.data.length; i++){
        	// 	var key = Object.keys(respon.data[i]); // Mencari key json
        	// 	// console.log(key[0]);
        	// 	if (key[0]= "status_upload") {
        	// 		$("#npwp_perusahaan").hide(1000)
        	// 	}else{
            // 		var val = respon.data[i][key[0]] // mencari value json
            // 		// console.log(key[0]+"_konfirmasi");
            // 		var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi

            // 		$(id).text(val);
            // 	}
        	// }	
        	var percentVal = '100%';
	        percent_berkas_akta_pendirian.html(percentVal);												
		}
		else{
			$('#checkbox_berkas_akta_pendirian').prop('checked', false);
			// console.log(respon);
        	// console.log(typeof respon);
        	var a = Object.keys(respon);
        	// console.log(respon['nama_lengkap'][0]['message']);
        	// console.log(a.length);
        	for (var i = 0; i < a.length; i++){
        		// console.log(a[i]);
        		// console.log(respon[a[i]]);
        		var field = a[i].replace("_", " ").capitalize();
        		toastr["error"](field+", "+respon[a[i]][0]['message'])
        		$("#"+a[i]+"").addClass("has-error");
        		// console.log($("#"+a[i]+"").addClass("parsley-error"));
        	btn_berkas_akta_pendirian.show();
    		percent_berkas_akta_pendirian.hide();
        	}
		}
	}
	});

	// berkas akta perubahan
	
	var btn_berkas_akta_perubahan = $('#btn_berkas_akta_perubahan');
	var percent_berkas_akta_perubahan = $('#percent_berkas_akta_perubahan');

	$("#form_berkas_akta_perubahan").ajaxForm({
		beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_akta_perubahan.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
    	btn_berkas_akta_perubahan.hide();
    	percent_berkas_akta_perubahan.show();
        var percentVal = percentComplete + '%';
        percent_berkas_akta_perubahan.html(percentVal);
    },
		success: function (response){
		respon = $.parseJSON(response)
		if(respon.success){
        	toastr["success"](respon.pesan)
			$('#checkbox_berkas_akta_pembaruan').prop('checked', true);
        	// $.cookie("keys", "value"); set cookie
        	// for (var i = 0; i < respon.data.length; i++){
        	// 	var key = Object.keys(respon.data[i]); // Mencari key json
        	// 	// console.log(key[0]);
        	// 	if (key[0]= "status_upload") {
        	// 		$("#npwp_perusahaan").hide(1000)
        	// 	}else{
            // 		var val = respon.data[i][key[0]] // mencari value json
            // 		// console.log(key[0]+"_konfirmasi");
            // 		var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi

            // 		$(id).text(val);
            // 	}
        	// }	
        	var percentVal = '100%';
	        percent_berkas_akta_perubahan.html(percentVal);												
		}
		else{
			$('#checkbox_berkas_akta_pembaruan').prop('checked', false);
			btn_berkas_akta_perubahan.show();
    		percent_berkas_akta_perubahan.hide();
			// console.log(respon);
        	// console.log(typeof respon);
        	var a = Object.keys(respon);
        	// console.log(respon['nama_lengkap'][0]['message']);
        	// console.log(a.length);
        	for (var i = 0; i < a.length; i++){
        		// console.log(a[i]);
        		// console.log(respon[a[i]]);
        		var field = a[i].replace("_", " ").capitalize();
        		toastr["error"](field+", "+respon[a[i]][0]['message'])
        		$("#"+a[i]+"").addClass("has-error");
        		// console.log($("#"+a[i]+"").addClass("parsley-error"));
        	}
		}
	}
	});

	// berkas pendukung
	
	var btn_berkas_pendukung = $('#btn_berkas_pendukung');
	var percent_berkas_pendukung = $('#percent_berkas_pendukung');

	$("#form_berkas_pendukung").ajaxForm({

		beforeSend: function() {
        var percentVal = '0%';
        percent_berkas_pendukung.html(percentVal);
    },
    uploadProgress: function(event, position, total, percentComplete) {
    	btn_berkas_pendukung.hide();
    	percent_berkas_pendukung.show();
        var percentVal = percentComplete + '%';
        percent_berkas_pendukung.html(percentVal);
    },
		success: function (response){
		respon = $.parseJSON(response)
		if(respon.success){
        	toastr["success"](respon.pesan)
			$('#checkbox_berkas_pendukung').prop('checked', true);
        	// $.cookie("keys", "value"); set cookie
        	for (var i = 0; i < respon.data.length; i++){
        		var key = Object.keys(respon.data[i]); // Mencari key json
        		// console.log(key[0]);
        		if (key[0]= "status_upload") {
        			$("#npwp_perusahaan").hide(1000)
        		}else{
            		var val = respon.data[i][key[0]] // mencari value json
            		// console.log(key[0]+"_konfirmasi");
            		var id = "#"+key[0]+"_konfirmasi" // membuat variabel id untuk sett ke id masing2 komfirmasi

            		$(id).text(val);
            	}
        	}	
        	var percentVal = '100%';
	        percent_berkas_pendukung.html(percentVal);												
		}
		else{
			$('#checkbox_berkas_pendukung').prop('checked', false);
			// console.log(respon);
        	// console.log(typeof respon);
        	var a = Object.keys(respon);
        	// console.log(respon['nama_lengkap'][0]['message']);
        	// console.log(a.length);
        	for (var i = 0; i < a.length; i++){
        		// console.log(a[i]);
        		// console.log(respon[a[i]]);
        		var field = a[i].replace("_", " ").capitalize();
        		toastr["error"](field+", "+respon[a[i]][0]['message'])
        		$("#"+a[i]+"").addClass("has-error");
        		// console.log($("#"+a[i]+"").addClass("parsley-error"));
        	btn_berkas_pendukung.show();
    		percent_berkas_pendukung.hide();
        	}
		}
	}
	});