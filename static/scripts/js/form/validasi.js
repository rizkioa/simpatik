$(".tanggal").mask("99-99-9999",{placeholder:"dd-mm-yyyy"});
$(".npwp").mask("99.999.999.9-999.999");
$(".kodepos").mask("99999");
$('.no_ktp').on('keydown', function(e){-1!==$.inArray(e.keyCode,[46,8,9,27,13,110,190])||/65|67|86|88/.test(e.keyCode)&&(!0===e.ctrlKey||!0===e.metaKey)||35<=e.keyCode&&40>=e.keyCode||(e.shiftKey||48>e.keyCode||57<e.keyCode)&&(96>e.keyCode||105<e.keyCode)&&e.preventDefault()});
$(".percent1").mask("9?9%");
$(".percent1").on("blur", function() {
    var value = $(this).val().length == 1 ? $(this).val() + '%' : $(this).val();
    $(this).val( value );
})