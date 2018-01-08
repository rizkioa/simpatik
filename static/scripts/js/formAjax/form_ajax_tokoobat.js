$('.kuasa_disable').prop('disabled', true).trigger("chosen:updated");
$("#switch_pemohon_disabled").change(function() {
  if ($(this).is(':checked')) {
    $('.kuasa_disable').prop('disabled', false).trigger("chosen:updated");
  }
  else {
    $('.kuasa_disable').prop('disabled', true).trigger("chosen:updated");
  }
});