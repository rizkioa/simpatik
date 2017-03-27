function load_perusahaan_a(npwp_){
	if (npwp_ !== ""){
		$(".tab-content").mLoading();
		csrf_token = $("input[name='csrfmiddlewaretoken']").val();
		$.ajax({
			type: 'POST',
			url: __base_url__+'/load-perusahaan/'+npwp_,
			data: { csrfmiddlewaretoken: csrf_token },
			success: function (data) {
	  			respon = $.parseJSON(data)
	    		if(respon.success){
		          	// load_provinsi1(respon.data.negara)
		          	// load_kabupaten1(respon.data.provinsi)
		          	// load_kecamatan1(respon.data.kabupaten)
		          	load_desa1(respon.data.kecamatan)
		          	setTimeout(function(){
			          	$('#id_kecamatan1').val(respon.data.kecamatan).prop('selected',true).trigger("chosen:updated");
		              	$('#id_desa1').val(respon.data.desa).prop('selected',true).trigger("chosen:updated");
		            }, 1000);
	              	$('#id_nama_perusahaan').val(respon.data.nama_perusahaan);
	              	$('#alamat_perusahaan_load').val(respon.data.alamat_perusahaan);
	              	$('#kode_pos_perusahaan_load').val(respon.data.kode_pos);
	              	$('#no_telepon_perusahaan_load').val(respon.data.telepon);
	              	$('#id_email_perusahaan').val(respon.data.email);
	              	$('#id_fax_perusahaan').val(respon.data.fax)
	              	// $('#id_negara1').val(respon.data.negara).prop('selected',true).trigger("chosen:updated");
	              	// $('#id_provinsi1').val(respon.data.provinsi).prop('selected',true).trigger("chosen:updated");
	              	// $('#id_kabupaten1').val(respon.data.kabupaten).prop('selected',true).trigger("chosen:updated");
	              	$('#switch_akta_pendirian_disabled').prop( "checked", true );
				  	setTimeout(function(){

		              	if (respon.data.legalitas_pendirian_nama_notaris !== ""){
		              		// +++++++ legalitas pendirian ++++++++
		              		$('#form-akta_pendirian').show()
		              		$.cookie("id_legalitas", respon.data.legalitas_pendirian_id, { path: '/' })
		              		$('#switch_akta_pendirian_disabled').prop( "checked", true );
						    $('.akta_pendirian_disable').prop('disabled', false);
						    $('#id_nama_notaris_legalitas_pendirian').val(respon.data.legalitas_pendirian_nama_notaris);
						    $('#id_alamat_legalitas_pendirian').val(respon.data.legalitas_pendirian_alamat);
						    $('#id_telp_legalitas_pendirian').val(respon.data.legalitas_pendirian_telephone);
						    $('#id_nomor_akta_legalitas_pendirian').val(respon.data.legalitas_pendirian_no_akta);
						    $('#id_tanggal_akta_legalitas_pendirian').val(respon.data.legalitas_pendirian_tanggal_akta);
						    $('#id_nomor_pengesahan_legalitas_pendirian').val(respon.data.legalitas_pendirian_no_pengesahan);
						    $('#id_tanggal_pengesahan_legalitas_pendirian').val(respon.data.legalitas_pendirian_tanggal_pengesahan);
			              	// +++++++ end legalitas pendirian ++++++++
		              	}
		              	else{
		              		$('#switch_akta_pendirian_disabled').prop( "checked", false );
		              		$('#form-akta_pendirian').hide()
		              		$.cookie("id_legalitas", "0", { path: '/' })
		              	}
		              	
		              	if(respon.data.legalitas_perubahan_nama_notaris !== ""){
		              		// ++++++ legalitas perubahan ++++++++
		              		$.cookie("id_legalitas_perubahan", respon.data.legalitas_perubahan_id, { path: '/' })
		              		$('#form-akta_perubahan').show()
		              		$('#field-akta_perubahan .berkas_kosong').prop('required',false);
			              	$('#switch_akta_perubahan_disabled').prop( "checked", true );
						    $(".akta_perubahan_disable").prop('disabled', false)
						    $('#id_nama_notaris_perubahan').val(respon.data.legalitas_perubahan_nama_notaris);
						    $('#id_alamat_notaris_perubahan').val(respon.data.legalitas_perubahan_alamat);
						    $('#id_telephone_notaris_perubahan').val(respon.data.legalitas_perubahan_telephone);
						    $('#id_nomor_akta_perubahan').val(respon.data.legalitas_perubahan_no_akta);
						    $('#id_tanggal_akta_perubahan').val(respon.data.legalitas_perubahan_tanggal_akta);
						    $('#id_nomor_pengesahan_perubahan').val(respon.data.legalitas_perubahan_no_pengesahan);
						    $('#id_tanggal_pengesahan_perubahan').val(respon.data.legalitas_perubahan_tanggal_pengesahan);
			              	// ++++++ end legalitas perubahan ++++++++
		              	}
		              	else{
		              		$('#switch_akta_perubahan_disabled').prop( "checked", false );
		              		$('#form-akta_perubahan').hide()
		              		$.cookie("id_legalitas_perubahan", "0", { path: '/' })
		              	}

		              	if(respon.data.legalitas_3_no_pengesahan !== ""){
		              		$('#field-akta_pengesahan_menteri .berkas_kosong').prop('required',false);
		              		$('#form-akta_pengesahan_menteri').show()
		              		$('#tr-akta_perubahan').show()
		              		$('.stap5_pengesahan_menteri').prop('disabled', false)
		              		$('#switch_stap5_pengesahan_menteri_disabled').prop( "checked", true );
		              		$('#id_nomor_pengesahan_pengesahan_menteri').val(respon.data.legalitas_3_no_pengesahan)
		              		$('#id_tanggal_pengesahan_pengesahan_menteri').val(respon.data.legalitas_3_tanggal_pengesahan)
		              	}
		              	else{
		              		$('#form-akta_pengesahan_menteri').hide()
		              		$('.stap5_pengesahan_menteri').prop('disabled', true)
		              		$('#switch_stap5_pengesahan_menteri_disabled').prop( "checked", false );
		              		$('#tr-akta_perubahan').hide()
		              	}

		              	if(respon.data.legalitas_4_no_pengesahan !== ""){
		              		$('#field-akta_persetujuan_menteri .berkas_kosong').prop('required',false);
		              		$('#form-akta_persetujuan_menteri').show()
		              		$('#tr-akta_pengesahan_menteri').show()
		              		$('.stap5_persetujuan_menteri').prop('disabled', false)
		              		$('#switch_stap5_persetujuan_menteri_disabled').prop( "checked", true );
		              		$('#id_nomor_pengesahan_persetujuan_menteri').val(respon.data.legalitas_4_no_pengesahan)
		              		$('#id_tanggal_pengesahan_persetujuan_menteri').val(respon.data.legalitas_4_tanggal_pengesahan)
		              	}
		              	else{
		              		$('#form-akta_persetujuan_menteri').hide()
		              		$('.stap5_persetujuan_menteri').prop('disabled', true)
		              		$('#switch_stap5_persetujuan_menteri_disabled').prop( "checked", false );
		              		$('#tr-akta_pengesahan_menteri').hide()
		              	}

		              	if(respon.data.legalitas_6_no_pengesahan !== ""){
		              		$('#field-akta_penerimaan_laporan .berkas_kosong').prop('required',false);
		              		$('#form-akta_penerimaan_laporan').show()
		              		$('#tr-akta_persetujuan_menteri').show()
		              		$('.stap5_penerima_laporan').prop('disabled', false)
		              		$('#switch_stap5_penerima_laporan_disabled').prop( "checked", true );
		              		$('#id_nomor_pengesahan_penerima_laporan').val(respon.data.legalitas_6_no_pengesahan)
		              		$('#id_tanggal_pengesahan_penerima_laporan').val(respon.data.legalitas_6_tanggal_pengesahan)
		              	}
		              	else{
		              		$('#form-akta_penerimaan_laporan').hide()
		              		$('.stap5_penerima_laporan').prop('disabled', true)
		              		$('#switch_stap5_penerima_laporan_disabled').prop( "checked", false );
		              	}

		              	if(respon.data.legalitas_7_no_pengesahan !== ""){
		              		$('#field-akta_penerimaan_pemberitahuan .berkas_kosong').prop('required',false);
		              		$('#form-akta_penerimaan_pemberitahuan').show()
		              		$('#tr-akta_penerimaan_laporan').show()
		              		$('.stap5_penerima_pemberitahuan').prop('disabled', false)
		              		$('#switch_stap5_penerima_pemberitahuan_disabled').prop( "checked", true );
		              		$('#id_nomor_pengesahan_penerimaan_pemberitahuan').val(respon.data.legalitas_7_no_pengesahan)
		              		$('#id_tanggal_pengesahan_penerimaan_pemberitahuan').val(respon.data.legalitas_7_tanggal_pengesahan)
		              	}
		              	else{
		              		$('#form-akta_penerimaan_pemberitahuan').hide()
		              		$('.stap5_penerima_pemberitahuan').prop('disabled', true)
		              		$('#switch_stap5_penerima_pemberitahuan_disabled').prop( "checked", false );
		              		$('#tr-akta_penerimaan_laporan').hide()
		              	}

		              	if(respon.data.legalitas_8_no_pengesahan !== ""){
		              		$('#field-akta_pengesahan_menteri_koperasi .berkas_kosong').prop('required',false);
		              		$('#form-akta_pengesahan_menteri_koperasi').show()
		              		$('#tr-akta_pengesahan_menteri_koperasi').show()
		              		$('.stap5_pengesahan_menteri_koperasi').prop('disabled', false)
		              		$('#switch_stap5_pengesahan_menteri_koperasi_disabled').prop( "checked", true );
		              		$('#id_nomor_pengesahan_persetujuan_menteri').val(respon.data.legalitas_8_no_pengesahan)
		              		$('#id_tanggal_pengesahan_pengesahan_menteri_koperasi').val(respon.data.legalitas_8_tanggal_pengesahan)
		              	}
		              	else{
		              		$('#form-akta_pengesahan_menteri_koperasi').hide()
		              		$('.stap5_pengesahan_menteri_koperasi').prop('disabled', true)
		              		$('#switch_stap5_pengesahan_menteri_koperasi_disabled').prop( "checked", false );
		              		$('#tr-akta_pengesahan_menteri_koperasi').hide()
		              	}

		              	if(respon.data.legalitas_9_no_pengesahan !== ""){
		              		$('#field-akta_persetujuan_menteri_koperasi .berkas_kosong').prop('required',false);
		              		$('#form-akta_persetujuan_menteri_koperasi').show()
		              		$('#tr-akta_persetujuan_menteri_koperasi').show()
		              		$('.stap5_persetujuan_menteri_koperasi').prop('disabled', false)
		              		$('#switch_stap5_persetujuan_menteri_koperasi_disabled').prop( "checked", true );
		              		$('#id_nomor_pengesahan_persetujuan_menteri_koperasi').val(respon.data.legalitas_8_no_pengesahan)
		              		$('#id_tanggal_pengesahan_persetujuan_menteri_koperasi').val(respon.data.legalitas_8_tanggal_pengesahan)
		              	}
		              	else{
		              		$('#form-akta_persetujuan_menteri_koperasi').hide()
		              		$('.stap5_persetujuan_menteri_koperasi').prop('disabled', true)
		              		$('#switch_stap5_persetujuan_menteri_koperasi_disabled').prop( "checked", false );
		              		$('#tr-akta_persetujuan_menteri_koperasi').hide()
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
		          	$.cookie("id_legalitas", "0", { path: '/' })
		          	$.cookie("id_legalitas_perubahan", "0", { path: '/' })
		        }
	      		$(".tab-content").mLoading('hide');
	    	},

		    error: function(data) {
		      toastr["error"]("Terjadi kesalahan pada koneksi server. Coba reload ulang browser Anda. ")
		      $(".tab-content").mLoading('hide');
		    }
		});
	}
}

function load_kecamatan1(id_kabupaten){
	csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	$( "#id_kecamatan1_chosen" ).mLoading();
	// $( "#id_kecamatan1_chosen .loadmask-msg" ).css('top', '2px')
	$.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kabupaten: id_kabupaten }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_kecamatan' %}', // the file to call
        url: __base_url__+'/admin/master/kecamatan/option/',
        success: function(response) { // on success..
          	elem = $( "#id_kecamatan1" )
          	elem.html(response);
          	make_disabled(elem, false)
          	$( "#id_kecamatan1_chosen" ).mLoading('hide');
          	$( "#id_kecamatan1" ).change(function(){
            $this = $(this)
            
            id_kecamatan1 = $(this).val()
            if(id_kecamatan1.length > 0){
              	load_desa1(id_kecamatan1)
            }
            else{
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
    $( "#id_desa1_chosen" ).mLoading();
	// $( "#id_desa_chosen1 .loadmask-msg" ).css('top', '2px')
	$.ajax({ // create an AJAX call...
        data: { csrfmiddlewaretoken: csrf_token, kecamatan: id_kecamatan }, // get the form data
        type: 'POST', // GET or POST
        // url: '{% url 'admin:option_desa' %}', // the file to call
        url: __base_url__+'/admin/master/desa/option/',
        success: function(response) { // on success..
          	elem = $( "#id_desa1" )
          	elem.html(response);
          	make_disabled(elem, false)
          	$( "#id_desa1_chosen" ).mLoading('hide');
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
		make_disabled($( "#id_desa1" ), true)
	  	
	}else{
		elem = $( "#id_kecamatan1" )
		make_disabled(elem, true)
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
	if ($('#alamat_perusahaan_load').val() === ""){
		$('#alamat_perusahaan_load').val(alamat);
	}
}