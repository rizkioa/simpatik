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
	var centang = $('#centang_operator').val();
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