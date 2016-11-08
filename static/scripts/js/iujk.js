function penanggung_jawab_add(){
	var elem_ = $('#penanggung_jawab')
	elem_.modal('show');
}

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
            row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[0]+'" target="blank_"> <i class="fa fa-check"></i> Foto </a></td>'
            row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[1]+'" target="blank_"> <i class="fa fa-check"></i> KTP </a></td>'
            row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[2]+'" target="blank_"> <i class="fa fa-check"></i> Pernyataan </a></td>'
            row += '<td align="center"><a class="btn btn-success btn-xs" href="'+split[3]+'" target="blank_"> <i class="fa fa-check"></i> Pernyataan </a></td>'
            // <td align="center"><i class="fa fa-check"></i></td> <td align="center"><i class="fa fa-check"></i></td> <td align="center"><i class="fa fa-check"></i></td> 
            row += '</tr>'
            $('#id_penanggung_jawab > tbody').prepend(row);

            toastr["success"](resp.pesan)
            penanggung_jawab_cancel();
          }else{
            // console.log(resp)
            if (resp["Terjadi Kesalahan"]) {
              toastr["warning"](resp["Terjadi Kesalahan"][0]['message'])
              $("#penanggung_jawab_form").trigger('reset');
              $('#penanggung_jawab_form').parsley().reset();
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
      toastr["warning"]("Silhkan Lengkapi Form")
    }
  btn_.html('<i class="fa fa-arrow-right"></i> Simpan')
  btn_.attr('disabled',false)
}

function penanggung_jawab_delete(btn_) {
    btn_.html("Tunggu...")
    btn_.attr('disabled',true)
    
    var ids = [];
    var ch = $('#id_penanggung_jawab').find('tbody input[type=checkbox]');
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
        toastr["warning"]("Anda belum memilih Direktur / Penanggung Jawab Badan Usaha")
    }

    btn_.html('Hapus <i class="fa fa-trash"></i>')
    btn_.attr('disabled',false)

    return false;
}
