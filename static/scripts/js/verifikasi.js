function verifikasi_operator(id_detil_siup, aksi){
	var centang = $('#centang_operator').val();
		csrf_token = $("input[name='csrfmiddlewaretoken']").val();
		if ($('#centang_operator').is(":checked")){
		$.ajax({ // create an AJAX call...
					data: { csrfmiddlewaretoken: csrf_token, id_detil_siup: id_detil_siup, aksi: aksi }, // get the form data
					type: 'POST', // GET or POST
					url: '/admin/izin/pengajuanizin/aksi/', // the file to call
					success: function(response) { // on success..
						respon = $.parseJSON(response)
						if(respon.success){
									toastr["success"](respon.pesan)
									window.location.href= "";
								}
								else{
										toastr["error"](respon.pesan)
								}
					},
					error: function(data) {
						alert('{{ pengajuan.id }}')                
							toast_server_error()
					}
		 });
		}
		else{
			toastr["warning"]("Anda belum menyentang persetujuan.")
		}
 
}

function verifikasi_kabid(id_detil_siup, aksi){
	var centang = $('#centang_kabid').val();
		csrf_token = $("input[name='csrfmiddlewaretoken']").val();
		if ($('#centang_kabid').is(":checked")){
			$.ajax({ // create an AJAX call...
					data: { csrfmiddlewaretoken: csrf_token, id_detil_siup: id_detil_siup, aksi: aksi }, // get the form data
					type: 'POST', // GET or POST
					url: '/admin/izin/pengajuanizin/aksi/', // the file to call
					success: function(response) { // on success..
						respon = $.parseJSON(response)
						if(respon.success){
									toastr["success"](respon.pesan)
									window.location.href= "";
								}
								else{
										toastr["error"](respon.pesan)
								}
					},
					error: function(data) {                
							toast_server_error()
					}
			});
		}
		else{
			toastr["warning"]("Anda belum menyentang persetujuan.")
		}
}

function create_skizin(id_detil_siup){
		csrf_token = $("input[name='csrfmiddlewaretoken']").val();
		$.ajax({ // create an AJAX call...
				data: { csrfmiddlewaretoken: csrf_token, id_detil_siup: id_detil_siup }, // get the form data
				type: 'POST', // GET or POST
				url: '/admin/izin/pengajuanizin/create-skizin/', // the file to call
				success: function(response) { // on success..
					respon = $.parseJSON(response)
					if(respon.success){
								toastr["success"](respon.pesan)
								window.location.href= "";
						}
						else{
								toastr["error"](respon.pesan)
						}
				},
				error: function(data) {                
						toast_server_error()
				}
		});
}

function verifikasi_skizin_kabid(id_detil_siup, aksi){
	var centang = $('#centang_skizin_kabid').val();
		csrf_token = $("input[name='csrfmiddlewaretoken']").val();
		if ($('#centang_skizin_kabid').is(":checked")){
		$.ajax({ // create an AJAX call...
					data: { csrfmiddlewaretoken: csrf_token, id_detil_siup: id_detil_siup, aksi: aksi }, // get the form data
					type: 'POST', // GET or POST
					url: '/admin/izin/pengajuanizin/aksi/', // the file to call
					success: function(response) { // on success..
						respon = $.parseJSON(response)
						if(respon.success){
										toastr["success"](respon.pesan)
										window.location.href= "";
								}
								else{
										toastr["error"](respon.pesan)
								}
					},
					error: function(data) {                
							toast_server_error()
					}
			});
		}
		else{
			toastr["warning"]("Anda belum menyentang persetujuan.")
		}
}

function verifikasi_kadin_to_kasir(id_detil_siup, aksi){
	var centang = $('#centang_skizin_kadin').val();
		csrf_token = $("input[name='csrfmiddlewaretoken']").val();
		if ($('#centang_skizin_kadin').is(":checked")){
		$.ajax({ // create an AJAX call...
					data: { csrfmiddlewaretoken: csrf_token, id_detil_siup: id_detil_siup, aksi: aksi }, // get the form data
					type: 'POST', // GET or POST
					url: '/admin/izin/pengajuanizin/aksi/', // the file to call
					success: function(response) { // on success..
						respon = $.parseJSON(response)
						if(respon.success){
									toastr["success"](respon.pesan)
									window.location.href= "";
								}
								else{
										toastr["error"](respon.pesan)
								}
					},
					error: function(data) {                
							toast_server_error()
					}
			});
		}
		else{
			toastr["warning"]("Anda belum menyentang persetujuan.")
		}
}

function verifikasi_skizin_kadin(id_detil_siup, aksi){
	var centang = $('#centang_skizin_kadin').val();
		csrf_token = $("input[name='csrfmiddlewaretoken']").val();
		if ($('#centang_skizin_kadin').is(":checked")){
		$.ajax({ // create an AJAX call...
					data: { csrfmiddlewaretoken: csrf_token, id_detil_siup: id_detil_siup, aksi: aksi }, // get the form data
					type: 'POST', // GET or POST
					url: '/admin/izin/pengajuanizin/aksi/', // the file to call
					success: function(response) { // on success..
						respon = $.parseJSON(response)
						if(respon.success){
									toastr["success"](respon.pesan)
									window.location.href= "";
								}
								else{
										toastr["error"](respon.pesan)
								}
					},
					error: function(data) {                
							toast_server_error()
					}
			});
		}
		else{
			toastr["warning"]("Anda belum menyentang persetujuan.")
		}
}

function penomoran_izin(id_detil_siup, aksi){
	var kode_jenis_izin = $('#kode_jenis_izin').val()
	var kode_izin = $('#penomoran_kode_izin').val()
	var tahun = $('#penomoran_tahun').val()
	var nomor_izin_sk = $('#nomor_izin_sk').val()
		csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	$.ajax({ // create an AJAX call...
			data: { csrfmiddlewaretoken: csrf_token, id_detil_siup: id_detil_siup, aksi: aksi, kode_jenis_izin: kode_jenis_izin, kode_izin: kode_izin,nomor_izin_sk: nomor_izin_sk, tahun: tahun }, // get the form data
			type: 'POST', // GET or POST
			url: '/admin/izin/pengajuanizin/aksi/', // the file to call
				success: function(response) { // on success..
						respon = $.parseJSON(response)
						if(respon.success){
							toastr["success"](respon.pesan)
							window.location.href= "";
						}
						else{
										toastr["error"](respon.pesan)
								}
				},
				error: function(data) {                
						toast_server_error()
				}
			})
}


function izin_selesai(id_detil_siup, aksi){
		csrf_token = $("input[name='csrfmiddlewaretoken']").val();
		if ($('#centang_selsai_izin').is(":checked")){
			$.ajax({ // create an AJAX call...
				data: { csrfmiddlewaretoken: csrf_token, id_detil_siup: id_detil_siup, aksi: aksi }, // get the form data
				type: 'POST', // GET or POST
				url: '/admin/izin/pengajuanizin/aksi/', // the file to call
				success: function(response) { // on success..
						respon = $.parseJSON(response)
						if(respon.success){
								toastr["success"](respon.pesan)
								window.location.href= "";
						}
						else{
										toastr["error"](respon.pesan)
								}
				},
				error: function(data) {                
						toast_server_error()
				}
		});
		}
		else{
			toastr["warning"]("Anda belum menyentang persetujuan.")
		}
}



$("#form_penolakan_verifikasi_kabid").ajaxForm({
	success: function (response){
		respon = $.parseJSON(response)
		if(respon.success){
			if(respon.success){
				toastr["warning"](respon.pesan)
				window.location.href= "";
			}												
		}
		else{
			toastr["error"](respon.pesan)
		}
	},
	error: function(data) {                
		toast_server_error()
	}
});

$("#form_perbaiki_draft_skizin").ajaxForm({
	success: function (response){
		respon = $.parseJSON(response)
		if(respon.success){
			if(respon.success){
				toastr["warning"](respon.pesan)
				window.location.href= "";
			}												
		}
		else{
			toastr["error"](respon.pesan)
		}
	},
	error: function(data) {                
		toast_server_error()
	}
});

function pembayaran_add(btn){
		var centang = $('#centang_operator').val();
		csrf_token = $("input[name='csrfmiddlewaretoken']").val();
		if ($('#centang_operator').is(":checked")){
			var frm = $('#id_form_pembayaran');
			if (frm.parsley().validate()){
				frm.ajaxSubmit({
				success: function(response) {  // on success..
				var respon = $.parseJSON(response);  
				if(respon.success){
					toastr["success"](respon.pesan)
					window.location.href= "";
				}
				else{
					toastr["error"](respon.pesan)
						}
					},
					error: function(data) {       
					toast_server_error()
				}
				});
			}
		}
		else{
			toastr["warning"]("Anda belum menyentang persetujuan.")
		}
	}

		function sk_add(btn){
				var frm = $('#id_form_sk');
				 if (frm.parsley().validate()){
						frm.ajaxSubmit({
						 success: function(response) {  // on success..
								var res = $.parseJSON(response);  
								$("#edit_skizin").modal('hide');
								},
								error: function(data) {       
									toast_server_error()
								}
							});
						}
			}

		function klasifikasi_jalan_add(btn){
				var frm = $('#id_form_klasifikasi_jalan');
				 if (frm.parsley().validate()){
						frm.ajaxSubmit({
						 success: function(response) {  // on success..
								var res = $.parseJSON(response);  
								$("#edit_klasifikasi_jalan").modal('hide');
								},
								error: function(data) {       
									toast_server_error()
								}
							});
						}
			}