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
	var kode_izin = $('#penomoran_kode_izin').val()
	var tahun = $('#penomoran_tahun').val()
  	csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	$.ajax({ // create an AJAX call...
	    data: { csrfmiddlewaretoken: csrf_token, id_detil_siup: id_detil_siup, aksi: aksi, kode_izin: kode_izin, tahun: tahun }, // get the form data
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

function cetak_izin(id_detil_siup, aksi){
	openPopupCenter('/admin/izin/pengajuanizin/cetak-siup-asli/'+id_detil_siup,'Preview Draft Surat {{pengajuan.pemohon.nama_lengkap}}', 1200, 600)
  	csrf_token = $("input[name='csrfmiddlewaretoken']").val();
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
	}
});