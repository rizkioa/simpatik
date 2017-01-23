function load_data_kebutuhan_lainnya(id_pengajuan){
  $(".tab-content").mLoading;
  if (id_pengajuan>0){
    $.ajax({
      url: __base_url__+'/imbreklame/load/'+id_pengajuan,    
      success: function (response){
        respon = $.parseJSON(response)  
        if (respon.success){
            $('#id_tenaga_ahli').val(respon.data.id_tenaga_ahli)

          }      
        },
        error: function(response){
        toast_server_error()
    }
    })
    }
}