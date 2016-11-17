function load_perusahaan_a(npwp_){
	$(".tab-content").mLoading();
	csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	$.ajax({
		type: 'POST',
		url: __base_url__+'/load-perusahaan/'+npwp_,
		data: { csrfmiddlewaretoken: csrf_token },
		success: function (data) {
  			$(".tab-content").mLoading('hide');
  			respon = $.parseJSON(data)
    		if(respon.success){
	          	// load_provinsi1(respon.data.negara)
	          	// load_kabupaten1(respon.data.provinsi)
	          	load_kecamatan1(respon.data.kabupaten)
	          	load_desa1(respon.data.kecamatan)
	          	
	              	$('#id_nama_perusahaan').val(respon.data.nama_perusahaan);
	              	$('#alamat_perusahaan_load').val(respon.data.alamat_perusahaan);
	              	$('#kode_pos_perusahaan_load').val(respon.data.kode_pos);
	              	$('#no_telepon_perusahaan_load').val(respon.data.telepon);
	              	$('#id_email_perusahaan').val(respon.data.email);
	              	$('#id_fax_perusahaan').val(respon.data.fax)
	              	// $('#id_negara1').val(respon.data.negara).prop('selected',true).trigger("chosen:updated");
	              	// $('#id_provinsi1').val(respon.data.provinsi).prop('selected',true).trigger("chosen:updated");
	              	// $('#id_kabupaten1').val(respon.data.kabupaten).prop('selected',true).trigger("chosen:updated");
	            setTimeout(function(){
	              	$('#id_kecamatan1').val(respon.data.kecamatan).prop('selected',true).trigger("chosen:updated");
	              	$('#id_desa1').val(respon.data.desa).prop('selected',true).trigger("chosen:updated");
	              	if (respon.data.npwp_perusahaan_url !== ''){
	              		$('#load_npwp_perusahaan').replaceWith("<span id='load_npwp_perusahaan' class='help-block' style='color:blue;'> file : <a target='_blank' href='"+respon.data.npwp_perusahaan_url+"'>"+respon.data.npwp_perusahaan_nama+"</a></span>")
	              		$('#checkbox_berkas_npwp_perusahaan').prop('checked', 1)
	              	}
	              	if (respon.data.legalitas_pendirian_url !== ''){
	              		$('#load_akta_pendirian').replaceWith("<span id='load_akta_pendirian' class='help-block' style='color:blue;'> file : <a target='_blank' href='"+respon.data.legalitas_pendirian_url+"'>"+respon.data.legalitas_pendirian_nama+"</a></span>")
	              		$('#checkbox_berkas_akta_pendirian').prop('checked', 1)
	              	}
	              	if (respon.data.legalitas_perubahan_url !== ''){
	              		$('#load_akta_perubahan').replaceWith("<span id='load_akta_perubahan' class='help-block' style='color:blue;'> file : <a target='_blank' href='"+respon.data.legalitas_perubahan_url+"'>"+respon.data.legalitas_perubahan_nama+"</a></span>")
	              		$('#checkbox_berkas_akta_pembaruan').prop('checked', 1)
	              	}
	            }, 2000);
    		}
	        else{
	          	$('#id_nama_perusahaan').val("");
	          	$('#alamat_perusahaan_load').val("");
	          	$('#kode_pos_perusahaan_load').val("");
	          	$('#no_telepon_perusahaan_load').val("");
	          	$('#id_email_perusahaan').val("");
	          	$('#id_fax_perusahaan').val("");
	          	// $('#id_negara1').val("").prop('selected',true).trigger("chosen:updated");
	          	// $('#id_provinsi1').val("").prop('selected',true).trigger("chosen:updated");
	          	// $('#id_kabupaten1').val("").prop('selected',true).trigger("chosen:updated");
	          	$('#id_kecamatan1').val("").prop('selected',true).trigger("chosen:updated");
	          	$('#id_desa1').val("").prop('selected',true).trigger("chosen:updated");
	          	$('#load_npwp_perusahaan').replaceWith("<span id='load_npwp_perusahaan'></span>");
              	$('#checkbox_berkas_npwp_perusahaan').prop('checked', 0)
              	$('#load_akta_pendirian').replaceWith("<span id='load_akta_pendirian'></span>");
              	$('#checkbox_berkas_akta_pendirian').prop('checked', 0)
              	$('#load_akta_perubahan').replaceWith("<span id='load_akta_perubahan'></span>");
              	$('#checkbox_berkas_akta_pembaruan').prop('checked', 0)
	        }
      
    	},
	    error: function(data) {
	      toastr["error"]("Terjadi kesalahan pada koneksi server. Coba reload ulang browser Anda. ")
	      $(".tab-content").mLoading('hide');
	    }
	});
}

function load_kecamatan1(id_kabupaten){
	csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	$( "#id_kecamatan_chosen1" ).mask('loading')
	$( "#id_kecamatan_chosen1 .loadmask-msg" ).css('top', '2px')
	$.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kabupaten: 1 }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_kecamatan' %}', // the file to call
        url: __base_url__+'/admin/master/kecamatan/option/',
        success: function(response) { // on success..
          elem = $( "#id_kecamatan1" )
          elem.html(response);
          make_disabled(elem, false)
          $( "#id_kecamatan_chosen1" ).unmask()
          $( "#id_kecamatan1" ).change(function(){
            $this = $(this)
            
            id_kecamatan1 = $(this).val()
            if(id_kecamatan1.length > 0){
              load_desa1(id_kecamatan1)
            }else{
              elem = $( "#id_desa1" )
              make_disabled(elem, true)
            }
          })
        },
        error: function(data) {                
          toast_server_error()
        }
    });
}

function load_desa1(id_kecamatan){
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $( "#id_desa_chosen1" ).mask('loading')
	$( "#id_desa_chosen1 .loadmask-msg" ).css('top', '2px')
	$.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kecamatan: id_kecamatan }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_desa' %}', // the file to call
        url: __base_url__+'/admin/master/desa/option/',
        success: function(response) { // on success..
          elem = $( "#id_desa1" )
          elem.html(response);
          make_disabled(elem, false)
          $( "#id_desa_chosen1" ).unmask()
          $( "#id_desa1" ).change(function(){
              $this = $(this)
          })
        },
        error: function(data) {                
          toast_server_error()
        }
    });
}

make_disabled($( "#id_desa1" ), true)
$( "#id_kecamatan1" ).change(function(){
	$this = $(this)

	id_kecamatan1 = $(this).val()
	if(id_kecamatan1.length > 0){
	  	load_desa1(id_kecamatan1)
	}else{
		// elem = $( "#id_kecamatan3" )
		// make_disabled(elem, true)
		make_disabled($( "#id_desa1" ), true)
	}
})

function load_no_telepon(){
	var no = $('#no_telepon_pemohon_load').val();
	$('#no_telepon_perusahaan_load').val(no);
}

function load_alamat(){
    	// load_provinsi1($('#id_negara').val())
  //     	load_kabupaten1($('#id_provinsi').val())
      	// load_kecamatan1($('#id_kabupaten').val())
      	// load_desa1($('#id_kecamatan').val())
      	// setTimeout(function(){
      		// $('#id_negara1').val($('#id_negara').val()).prop('selected',true).trigger("chosen:updated");
        //   	$('#id_provinsi1').val($('#id_provinsi').val()).prop('selected',true).trigger("chosen:updated");
        //   	$('#id_kabupaten1').val($('#id_kabupaten').val()).prop('selected',true).trigger("chosen:updated");
//            	$('#id_kecamatan1').val($('#id_kecamatan').val()).prop('selected',true).trigger("chosen:updated");
//            	$('#id_desa1').val($('#id_desa').val()).prop('selected',true).trigger("chosen:updated");
//        	}, 1000);
	var alamat = $('#alamat_pemohon_load').val();
	$('#alamat_perusahaan_load').val(alamat);
}