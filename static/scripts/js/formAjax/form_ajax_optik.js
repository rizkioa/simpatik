$('.kuasa_disable').prop('disabled', true).trigger("chosen:updated");
$("#switch_pemohon_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.kuasa_disable').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.kuasa_disable').prop('disabled', true).trigger("chosen:updated");
  }
});
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
      url: __base_url__+'/izin-dinkes/optikal/load-berkas/ajax/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
        console.log(respon)
        if (respon.success) {
          len = respon.berkas.length
          for (var i = 0; i < len; i++) {
            // console.log(respon.berkas[i])
            // console.log(respon.elemen[i])
            // console.log(respon.id_berkas[i])
            // style="min-width: 742px;text-align: left;"
            url = '<a id="btn-load-'+respon.elemen[i]+'" class="btn btn-success btn-sm" data-toggle="popover" data-trigger="hover" data-container="body" data-placement="bottom" href="'+respon.berkas[i]+'" target="blank_"> <i class="fa fa-check"></i> '+respon.nm_berkas[i]+' </a> <a class="btn btn-danger btn-sm" onclick="delete_berkas_upload('+respon.id_berkas[i]+',\''+respon.elemen[i]+'\');return false;" > <i class="fa fa-trash"></i> Hapus</a>'
            // console.log(url)
            $('#load-'+respon.elemen[i]).html(url)
            $('#field-'+respon.elemen[i]+' .berkas_kosong').prop('required',false);
            // $('#field-'+respon.elemen[i]+' .berkas_kosong').val(__base_url__+respon.berkas[i]);
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
    url: url = __base_url__+'/ajax-delete-berkas-upload-tdp/'+id+'/'+elemen,
    success: function (response){
        respon = $.parseJSON(response)
        if (respon.success) {
          toastr["success"](respon.pesan)
          $('#form-'+elemen)[0].reset() 
          $('#percent-'+elemen).hide()
          $('#btn-'+elemen).show()
          $('#field-'+elemen+' .berkas_kosong').prop('required',true);
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