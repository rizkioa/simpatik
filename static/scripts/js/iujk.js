function load_klasifikasi(){
  csrf_token = $("input[name='csrfmiddlewaretoken']").val();
  elem = $("#klasifikasi")
  $.ajax({ // create an AJAX call...
      data: { csrfmiddlewaretoken: csrf_token }, // get the form data
      type: 'POST', // GET or POST
      url: __base_url__+'/admin/izin/detiliujk/option-klasifikasi/',
      success: function(response) { // on success..
          // console.log(response)
          elem.html(response);
      },
      error: function(data) {                
          toast_server_error()
      }
  });
}

function load_subklasifikasi(id_klasifikasi){
  csrf_token = $("input[name='csrfmiddlewaretoken']").val();
  elem = $("#subklasifikasi")
  $.ajax({ // create an AJAX call...
      data: { csrfmiddlewaretoken: csrf_token, klasifikasi: id_klasifikasi }, // get the form data
      type: 'POST', // GET or POST
      url: __base_url__+'/admin/izin/detiliujk/option-subklasifikasi/',
      success: function(response) { // on success..
          // console.log(response)
          elem.html(response);
      },
      error: function(data) {                
          toast_server_error()
      }
  });
}

// *********** SURVEY ***********
function survey_save(elem_){
  var btn_ = $('#button-'+elem_)
  btn_.html('Tunggu...')
  btn_.attr('disabled',true)
  var frm = $("#form-"+elem_);
  // console.log(frm.serialize())
  frm.parsley().validate();
  if (frm.parsley().isValid()) {
    frm.ajaxSubmit({
        method: 'POST',
        data: frm.serialize(),
        url: frm.attr('action'),
        success: function(response){
          resp = $.parseJSON(response)
          console.log(resp)

          if (resp.success){
            location.reload();
          }else{
            var a = Object.keys(respon);
            for (var i = 0; i < a.length; i++){
              var field = a[i].replace("_", " ");
              toastr["error"](field+", "+respon[a[i]][0]['message'])
              $("#"+a[i]+"").addClass("has-error");
            }
          }
          // btn_.html('<i class="fa fa-arrow-right"></i> Simpan')
          // btn_.attr('disabled',false)
        }
    })
  }else{
    btn_.html('<i class="fa fa-arrow-right"></i> Simpan')
    btn_.attr('disabled',false)
    toastr["warning"]("Silakan Lengkapi Form")
  }
}

function survey_delete(elem_){
  var btn_ = $('#delete-'+elem_)
  btn_.html('Tunggu...')
  btn_.attr('disabled',true)
  var ids = [];
  // var ch = $('#tabel_penanggung_jawab').find('tbody input[type=checkbox]');
  var ch = $('#tabel_survey').find('tbody input[type=checkbox]');
  ch.each(function () {
      if ($(this).is(":checked")) {
          ids.push($(this).val());
      }
  });

   if (ids.length) {
      for(var i=0; i < ids.length; i++){
        // LOOP AJAX DELETE
        $.ajax({
          method: 'POST',
          data: {id : ids[i], csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
          url: __base_url__+'/admin/izin/survey/survey-delete-ajax/',
          success: function(response){
            respon = $.parseJSON(response)
            if(respon.success){
              toastr["success"](respon.pesan)
              $('#'+respon.id).remove()
              location.reload();
              // console.log($('#'+respon.id).remove());
            }else{
              toastr["error"](respon.pesan)
            }
          },error: function(response){
            toast_server_error()
          }
        });
      }
      // btn_.html('Hapus <i class="fa fa-trash"></i>')
      // btn_.attr('disabled',false)
   }else {
        toastr["warning"]("Anda belum memilih Data Survey")
    }
}

function kirim_survey(id_pengajuan){
  $.ajax({
    method: 'POST',
    data: {id : id_pengajuan, csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
    url: __base_url__+'/admin/izin/survey/survey-sending/',
    success: function(response){
      respon = $.parseJSON(response)
      if(respon.success){
        toastr["success"](respon.pesan)
        location.reload();
        // console.log($('#'+respon.id).remove());
      }else{
        toastr["error"](respon.pesan)
      }
    },error: function(response){
      toast_server_error()
    }
  });
}

//************* END *********** 

function show_modal_dataanggota_add(elem_){
  // var elem_ = $('#penanggung_jawab')
  elem_.modal('show');
}
// **** PENANGGUNG JAWAB DIREKTUR ****


function penanggung_jawab_cancel(){
	var elem_ = $('#penanggung_jawab')
  $("#penanggung_jawab_form").trigger('reset');
  $('#penanggung_jawab_form').parsley().reset();
  $('.progresdirektur').hide();
  $('#dataprogresuploaddirektur').html('0');
  $('#progresuploaddirektur').css('width','0%');
  $('#progresuploaddirektur').attr('data-percentage','0%');
	elem_.modal('hide');
}


function penanggung_jawab_save(btn_){
  btn_.html("Tunggu...")
  btn_.attr('disabled',true)
  var frm = $("#penanggung_jawab_form");
    frm.parsley().validate();
    if (frm.parsley().isValid()) {
      // console.log("masuk valid");
      // alert(frm.attr('action'));
      
      frm.ajaxSubmit({
        method: 'POST',
        data: frm.serialize(),
        url: frm.attr('action'),
        beforeSend: function() {
          var percentVal = '0%';
          $('.progresdirektur').show();
          $('#dataprogresuploaddirektur').html(0);
          $('#progresuploaddirektur').css('width',percentVal);
          $('#progresuploaddirektur').attr('data-percentage',percentVal);
        },
        uploadProgress: function(event, position, total, percentComplete) {
          // console.log(percentComplete);
          var percentVal = percentComplete + '%';
          $('#dataprogresuploaddirektur').html(percentComplete);
          $('#progresuploaddirektur').css('width',percentVal);
          $('#progresuploaddirektur').attr('data-percentage',percentVal);
        },
        success: function(response){
          resp = $.parseJSON(response)
          if (resp.success){
            
            row = '<tr id="'+resp.data[0].id+'"> <td><input type="checkbox" value="'+resp.data[0].id+'" id="chkbox"></input></td> <td>'+resp.data[1].nama+'</td>'
            split = resp.data[2].berkas.split(",")
            row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[0]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
            row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[1]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
            row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[2]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
            row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[3]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
            // <td align="center"><i class="fa fa-check"></i></td> <td align="center"><i class="fa fa-check"></i></td> <td align="center"><i class="fa fa-check"></i></td> 
            row += '</tr>'
            $('#tabel_penanggung_jawab > tbody').prepend(row);

            toastr["success"](resp.pesan)
            penanggung_jawab_cancel();
          }else{
            // console.log(resp)
            if (resp["Terjadi Kesalahan"]) {
              toastr["warning"](resp["Terjadi Kesalahan"][0]['message'])
              frm.trigger('reset');
              frm.parsley().reset();
              $('.progresdirektur').hide();
            }else{
              
            }
            
          }
          
        },
        error: function(response){
          toast_server_error()
        }
      });
    }else{
      toastr["warning"]("Silakan Lengkapi Form")
    }
  btn_.html('<i class="fa fa-arrow-right"></i> Simpan')
  btn_.attr('disabled',false)
}

function penanggung_jawab_delete(btn_, elem_) {
    btn_.html("Tunggu...")
    btn_.attr('disabled',true)
    
    var ids = [];
    // var ch = $('#tabel_penanggung_jawab').find('tbody input[type=checkbox]');
    var ch = elem_.find('tbody input[type=checkbox]');
    ch.each(function () {
        if ($(this).is(":checked")) {
            ids.push($(this).val());
        }
    });
    // console.log(ids);
    if (ids.length) {
      for(var i=0; i < ids.length; i++){
      	// LOOP AJAX DELETE
      	$.ajax({
          method: 'POST',
          data: {id : ids[i], csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
          url: __base_url__+'/layanan/iujk/penanggungjawab/delete/',
          success: function(response){
            respon = $.parseJSON(response)
            if(respon.success){
              toastr["success"](respon.pesan)
              $('#'+respon.id).remove()
              // console.log($('#'+respon.id).remove());
            }else{
              toastr["error"](respon.pesan)
            }
          },error: function(response){
            toast_server_error()
          }
      	});
      }
    } else {
        toastr["warning"]("Anda belum memilih Anggota Badan Usaha")
    }

    btn_.html('Hapus <i class="fa fa-trash"></i>')
    btn_.attr('disabled',false)

    return false;
}

// **** END ****

// **** Tenaga teknik ****
function tenaga_teknik_cancel(){
  var elem_ = $('#teknik')
  $("#teknik_form").trigger('reset');
  $('#teknik_form').parsley().reset();
  $('.progresteknik').hide();
  $('#dataprogresteknik').html('0');
  $('#progresteknik').css('width','0%');
  $('#progresteknik').attr('data-percentage','0%');
  elem_.modal('hide');
}

function penanggung_jawab_teknik_save(btn_){
  // alert("aOKE")
  btn_.html("Tunggu...")
  btn_.attr('disabled',true)

  var frm = $("#teknik_form");
  frm.parsley().validate();
  if (frm.parsley().isValid()) {
    frm.ajaxSubmit({
      method: 'POST',
      data: frm.serialize(),
      url: frm.attr('action'),
      beforeSend: function() {
        var percentVal = '0%';
        $('.progresteknik').show();
        $('#dataprogresteknik').html(0);
        $('#progresteknik').css('width',percentVal);
        $('#progresteknik').attr('data-percentage',percentVal);
      },
      uploadProgress: function(event, position, total, percentComplete) {
        var percentVal = percentComplete + '%';
        $('#dataprogresteknik').html(percentComplete);
        $('#progresteknik').css('width',percentVal);
        $('#progresteknik').attr('data-percentage',percentVal);
      },
      success: function(response){
        resp = $.parseJSON(response)
        console.log(resp)
        if (resp.success){
          
          row = '<tr id="'+resp.data[0].id+'"> <td><input type="checkbox" value="'+resp.data[0].id+'" id="chkbox"></input></td> <td>'+resp.data[1].nama+'</td><td>'+resp.data[3].no_pjt_bu+'</td>'
          split = resp.data[2].berkas.split(",")
          row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[0]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
          row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[1]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
          row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[2]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
          row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[3]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
          row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[4]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
          // <td align="center"><i class="fa fa-check"></i></td> <td align="center"><i class="fa fa-check"></i></td> <td align="center"><i class="fa fa-check"></i></td> 
          row += '</tr>'
          $('#tabel_penanggung_jawab_teknik > tbody').prepend(row);

          toastr["success"](resp.pesan)
          tenaga_teknik_cancel();
        }else{
          // console.log(resp)
          if (resp["Terjadi Kesalahan"]) {
            toastr["warning"](resp["Terjadi Kesalahan"][0]['message'])
            frm.trigger('reset');
            frm.parsley().reset();
            $('.progresteknik').hide();
          }else{
            toast_server_error()
          }
        }
      },
      error: function(response){
        toast_server_error()
      }
    });
  }else{
    toastr["warning"]("Silakan Lengkapi Form")
  }

  btn_.html('<i class="fa fa-arrow-right"></i> Simpan')
  btn_.attr('disabled',false)

  return false;
}
// **** END ****

// **** Tenaga Non teknik ****
function tenaga_non_teknik_cancel(){
  var elem_ = $('#non_teknik')
  $("#non_teknik_form").trigger('reset');
  $('#non_teknik_form').parsley().reset();
  $('.progresnonteknik').hide();
  $('#dataprogresnonteknik').html('0');
  $('#progresnonteknik').css('width','0%');
  $('#progresnonteknik').attr('data-percentage','0%');
  elem_.modal('hide');
}

function penanggung_jawab_non_teknik_save(btn_){
  btn_.html("Tunggu...")
  btn_.attr('disabled',true)

  var frm = $("#non_teknik_form");
  frm.parsley().validate();
  if (frm.parsley().isValid()) {
    frm.ajaxSubmit({
      method: 'POST',
      data: frm.serialize(),
      url: frm.attr('action'),
      beforeSend: function() {
        var percentVal = '0%';
        $('.progresnonteknik').show();
        $('#dataprogresnonteknik').html(0);
        $('#progresnonteknik').css('width',percentVal);
        $('#progresnonteknik').attr('data-percentage',percentVal);
      },
      uploadProgress: function(event, position, total, percentComplete) {
        var percentVal = percentComplete + '%';
        $('#dataprogresnonteknik').html(percentComplete);
        $('#progresnonteknik').css('width',percentVal);
        $('#progresnonteknik').attr('data-percentage',percentVal);
      },
      success: function(response){
        resp = $.parseJSON(response)
        if (resp.success){
          
          row = '<tr id="'+resp.data[0].id+'"> <td><input type="checkbox" value="'+resp.data[0].id+'" id="chkbox"></input></td> <td>'+resp.data[1].nama+'</td>'
          split = resp.data[2].berkas.split(",")
          row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[0]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
          row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[1]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
          row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[2]+'" target="blank_"> <i class="fa fa-check"></i> Berkas </a></td>'
          // <td align="center"><i class="fa fa-check"></i></td> <td align="center"><i class="fa fa-check"></i></td> <td align="center"><i class="fa fa-check"></i></td> 
          row += '</tr>'
          $('#tabel_penanggung_jawab_non_teknik > tbody').prepend(row);

          toastr["success"](resp.pesan)
          tenaga_non_teknik_cancel();
        }else{
          // console.log(resp)
          if (resp["Terjadi Kesalahan"]) {
            toastr["warning"](resp["Terjadi Kesalahan"][0]['message'])
            frm.trigger('reset');
            frm.parsley().reset();
            $('.progresteknik').hide();
          }else{
            toast_server_error()
          }
        }
      },
      error: function(response){
        toast_server_error()
      }
    });
  }else{
    toastr["warning"]("Silakan Lengkapi Form")
  }

  btn_.html('<i class="fa fa-arrow-right"></i> Simpan')
  btn_.attr('disabled',false)

  return false;
}
// **** END ****


// ***** UPLOAD FORM *****
function form_upload_dokumen(elem_){
  var elem_ = elem_[0].id
  var split_ = elem_.split('-')[1]
  $(".tab-content").mLoading();
  var frm = $('#form-'+split_);
  // console.log(frm)

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
          toast_server_error()
          $('#percent-'+split_).hide();
          $('#btn-'+split_).show();
        }
      }
    },
    error: function(response){
      toast_server_error()
      $('#percent-'+split_).hide();
      $('#btn-'+split_).show();
    }
  })
  $(".tab-content").mLoading('hide');
}
// ***** END *****

// ***** Load Form Upload *****
function load_berkas(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/ajax-load-berkas/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          len = respon.berkas.length
          for (var i = 0; i < len; i++) {
            // console.log(respon.berkas[i])
            // console.log(respon.elemen[i])
            // console.log(respon.id_berkas[i])
            url = '<a id="btn-load-'+respon.elemen[i]+'" class="btn btn-success btn-sm" data-toggle="popover" data-trigger="hover" data-container="body" data-placement="bottom" href="'+respon.berkas[i]+'" target="blank_"> <i class="fa fa-check"></i> '+respon.nm_berkas[i]+' </a> <a class="btn btn-danger btn-sm" onclick="delete_berkas_upload('+respon.id_berkas[i]+',\''+respon.elemen[i]+'\');return false;" > <i class="fa fa-trash"></i> Hapus</a>'
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


// ****** KONFIRMASI *******
function load_konfirmasi(id_pengajuan){
  $(".tab-content").mLoading();
  if (id_pengajuan > 0){
    $('#tabel_klasifikasi_pekerjaan-konfirmasi > tbody').empty();
    $('#tabel_klasifikasi_pekerjaan-konfirmasi > tbody').html('<tr id=tabel_klasifikasi_pekerjaan-loading> <td colspan="4"> <i class="fa fa-spinner fa-spin"></i> Ambil Data... </td> </tr>')
    $.ajax({
      url: __base_url__+'/ajax-konfirmasi-paket-pekerjaan/'+id_pengajuan,
      success: function (response){
        
        respon = $.parseJSON(response)
        // console.log(a)
        if (respon.paket){
          keterangan = ''
          a = respon.paket.length
          $('#jenis_iujk_konfirmasi').html(respon.jenis)
          str = ""
          for (var i = 0; i < a; i++){
            // split = respon.berkas[i].split(",")
            // console.log(respon.paket[i])
            // console.log(respon.paket[i].klasifikasi)
            // console.log(respon.paket[i].subklasifikasi)
            // console.log(respon.paket[i].tahun)
            // console.log(respon.paket[i].nilai_paket_pekerjaan)
            if(respon.paket[i].keterangan !== null){
              // do something
              // console.log('asdf')
              keterangan = respon.paket[i].keterangan
            }else{
              // console.log("hahah")
            }
            str += '<tr>'
            str += '<td>'+respon.paket[i].klasifikasi+'</td>'
            str += '<td>'+respon.paket[i].subklasifikasi+'</td>'
            str += '<td>'+respon.paket[i].nama_paket_pekerjaan+'</td>'
            str += '<td>'+keterangan+'</td>'
            str += '<td>'+respon.paket[i].tahun+'</td>'
            str += '<td>'+respon.paket[i].nilai_paket_pekerjaan+'</td>'
            str += '</tr>'
          }
          $('#tabel_klasifikasi_pekerjaan-konfirmasi > tbody').html(str);
          $('#tabel_klasifikasi_pekerjaan-loading').remove();
        }
      }
    })

    $('#tabel_penanggung_jawab-konfirmasi > tbody').empty();
    $('#tabel_penanggung_jawab-konfirmasi > tbody').html('<tr id=tabel_penanggung_jawab-loading> <td colspan="4"> <i class="fa fa-spinner fa-spin"></i> Ambil Data... </td> </tr>')
    $.ajax({
      url: __base_url__+'/ajax-konfirmasi-anggota-badan-direktur/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        // console.log(a)
        if (respon.anggota){
          a = respon.anggota.length
          // console.log(respon.berkas.split(','))
          // berkas = respon.berkas.split(',')
          direktur = ""
          for (var i = 0; i < a; i++){
            
            
            // console.log(respon.anggota[i].jenis_anggota_badan)
            // console.log(respon.anggota[i].nama)
            // console.log(respon.anggota[i].id)
            // console.log(respon.anggota[i].berkas_tambahan)
            direktur = '<tr>'
            direktur += '<td>'+respon.anggota[i].nama+'</td>'
            direktur += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked></td>'
            direktur += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked></td>'
            direktur += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked></td>'
            direktur += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked></td>'
            direktur += '</tr>'
            $('#tabel_penanggung_jawab-konfirmasi > tbody').prepend(direktur);
            $('#tabel_penanggung_jawab-loading').remove();

          }
          
        }
      }
    })

    $('#tabel_penanggung_jawab_teknik-konfirmasi > tbody').empty();
    $('#tabel_penanggung_jawab_teknik-konfirmasi > tbody').html('<tr id=tabel_penanggung_jawab_teknik-loading> <td colspan="4"> <i class="fa fa-spinner fa-spin"></i> Ambil Data... </td> </tr>')
    $.ajax({
      url: __base_url__+'/ajax-konfirmasi-anggota-badan-teknik/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        // console.log(a)
        if (respon.anggota){
          a = respon.anggota.length
          teknik = ""
          for (var i = 0; i < a; i++){
            
            // console.log(respon.anggota[i].jenis_anggota_badan)
            // console.log(respon.anggota[i].nama)
            // console.log(respon.anggota[i].id)
            // console.log(respon.anggota[i].berkas_tambahan)
            teknik = '<tr>'
            teknik += '<td>'+respon.anggota[i].nama+'</td>'
            teknik += '<td>'+respon.anggota[i].no_pjt_bu+'</td>'
            teknik += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked>'
            teknik += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked>'
            teknik += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked>'
            teknik += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked>'
            teknik += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked>'
            teknik += '</tr>'
            $('#tabel_penanggung_jawab_teknik-konfirmasi > tbody').prepend(teknik);
            $('#tabel_penanggung_jawab_teknik-loading').remove();
          }
          
        }
      }
    })

    $('#tabel_penanggung_jawab_non_teknik-konfirmasi > tbody').empty();
    $.ajax({
      url: __base_url__+'/ajax-konfirmasi-anggota-badan-nonteknik/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        // console.log(a)
        if (respon.anggota){
          a = respon.anggota.length
          teknik = ""
          for (var i = 0; i < a; i++){
            
            // console.log(respon.anggota[i].jenis_anggota_badan)
            // console.log(respon.anggota[i].nama)
            // console.log(respon.anggota[i].id)
            // console.log(respon.anggota[i].berkas_tambahan)
            teknik = '<tr>'
            teknik += '<td>'+respon.anggota[i].nama+'</td>'
            teknik += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked>'
            teknik += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked>'
            teknik += '<td align="center"><input type="checkbox" id="checkbox-sertifikat" disabled="" checked>'
            teknik += '</tr>'
            $('#tabel_penanggung_jawab_non_teknik-konfirmasi > tbody').prepend(teknik);
          }
          
        }
      }
    })
  }
   $(".tab-content").mLoading('hide');
}
// ********* END ***********