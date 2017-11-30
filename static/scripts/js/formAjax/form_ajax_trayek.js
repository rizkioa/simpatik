
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
      url: __base_url__+'/layanan/izin-angkutan-trayek/load-berkas-pengajuanizin/'+id_pengajuan,
      success: function (response){
        respon = $.parseJSON(response)
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
    url: url = __base_url__+'/layanan/iua/ajax-delete-berkas-upload-iua/'+id+'/'+elemen,
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
// **** END *****

// **** Load Komfirmasi ****
function load_konfirmasi(pengajuan_id){
    // console.log(id_pengajuan)
    $.ajax({
      type: 'GET',
      url: __base_url__+'/layanan/iua/ajax-iua-load-konfirmasi/'+pengajuan_id,
      success: function(data){
        data_ = JSON.parse(data)
        console.log(data_)
        if(data_.success == true){
          $('#jenis_pengajuan_konfirmasi').text(data_.jenis_pengajuan)
          $('#jenis_pemohon_konfirmasi').text(data_.pemohon_json.jenis_pemohon)
          $('#nomor_ktp_konfirmasi').text(data_.pemohon_json.username)
          $('#nama_lengkap_konfirmasi').text(data_.pemohon_json.nama_lengkap)
          $('#alamat_konfirmasi').text(data_.pemohon_json.alamat)
          $('#telephone_konfirmasi').text(data_.pemohon_json.telephone)
          $('#hp_konfirmasi').text(data_.pemohon_json.hp)
          $('#email_konfirmasi').text(data_.pemohon_json.email)
          $('#kewarganegaraan_konfirmasi').text(data_.pemohon_json.kewarganegaraan)
          $('#pekerjaan_konfirmasi').text(data_.pemohon_json.pekerjaan)
          // **** perusahaan ****
          $('#npwp_perusahaan_konfirmasi').text(data_.perusahaan_json.npwp)
          $('#nama_perusahaan_konfirmasi').text(data_.perusahaan_json.nama_perusahaan)
          $('#alamat_perusahaan_konfirmasi').text(data_.perusahaan_json.alamat_lengkap)
          $('#kode_pos_perusahaan_konfirmasi').text(data_.perusahaan_json.kode_pos)
          $('#telepon_perusahaan_konfirmasi').text(data_.perusahaan_json.telepon)
          $('#fax_perusahaan_konfirmasi').text(data_.perusahaan_json.fax)
          $('#email_perusahaan_konfirmasi').text(data_.perusahaan_json.email)
          // **** kendaraan ****
          $('#nilai_investasi_konfirmasi').text(data_.nilai_investasi)
          $('#jenis_kendaraan_konfirmasi').text(data_.kategori_kendaraan)
          $('#jumlah_kendaraan_konfirmasi').text(data_.jumlah_kendaraan)
          $('#nomor_izin_ho').text(data_.detil_izin_ho)
          len1 = data_.kendaraan.length
          
          if(len1 > 0){
            for (var i=0; i<len1; i++){
              row = '<tr>'
              row += '<td>'+data_.kendaraan[i].nomor_kendaraan+'</td>'
              row += '<td>'+data_.kendaraan[i].nomor_uji_berkala+'</td>'
              row += '<td>'+data_.kendaraan[i].merk_kendaraan_nama+'</td>'
              row += '<td>'+data_.kendaraan[i].nomor_rangka+'</td>'
              row += '<td>'+data_.kendaraan[i].nomor_mesin+'</td>'
              row += '<td>'+data_.kendaraan[i].tahun_pembuatan+'</td>'
              row += '<td>'+data_.kendaraan[i].berat_diperbolehkan+'</td>'
              row += '<td>'+data_.kendaraan[i].keterangan+'</td>'
              row += '</tr>'
            } 
          }

          else{
            row = '<tr><td colspan="2" aling="center">Data Kosong ! </td></tr>'
            // $('#id_data_kendaraan > tbody').html(row)
          }
        }
        else{
          row = '<tr><td colspan="2" aling="center">Data Kosong ! </td></tr>'
          // $('#id_data_kendaraan > tbody').html(row)
        }
        $('#id_data_kendaraan > tbody').html(row)
        
      }
    })
  }
// **** END ****