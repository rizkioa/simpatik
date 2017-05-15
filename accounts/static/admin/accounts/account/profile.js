function make_disabled(elem_, dis_){
	if (dis_ == true){
		elem_.empty();
	}
	elem_.prop( "disabled", dis_);
	elem_.trigger("chosen:updated");
}

make_disabled($( "#id_provinsi" ), true)
make_disabled($( "#id_kabupaten" ), true)
make_disabled($( "#id_kecamatan" ), true)
make_disabled($( "#id_desa" ), true)
$( "#id_negara" ).change(function(){
	$this = $(this)
	id_negara = $(this).val()
	if(id_negara.length > 0){
		load_provinsi(id_negara)
		make_disabled($( "#id_provinsi" ), true)
		make_disabled($( "#id_kabupaten" ), true)
		make_disabled($( "#id_kecamatan" ), true)
		make_disabled($( "#id_desa" ), true)
	}else{
		make_disabled($( "#id_provinsi" ), true)
		make_disabled($( "#id_kabupaten" ), true)
		make_disabled($( "#id_kecamatan" ), true)
		make_disabled($( "#id_desa" ), true)
	}
})

function load_provinsi(id_negara){
	csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	$( "#id_provinsi_chosen" ).mLoading();
	// $( "#id_provinsi_chosen .loadmask-msg" ).css('top', '2px')
	$.ajax({ // create an AJAX call...
		data: { csrfmiddlewaretoken: csrf_token, negara: id_negara }, // get the form data
		type: 'POST', // GET or POST
		// url: '{% url 'admin:option_provinsi' %}', // the file to call
		url: __base_url__+'/admin/master/provinsi/option/',
		success: function(response) { // on success..
			elem = $( "#id_provinsi" )
			elem.html(response);
			make_disabled(elem, false)
			// $( "#id_provinsi_chosen" ).unmask()
			$( "#id_provinsi_chosen" ).mLoading('hide');
			$( "#id_provinsi" ).change(function(){
				$this = $(this)
				id_provinsi = $(this).val()
				if(id_provinsi.length > 0){
					load_kabupaten(id_provinsi)
				}else{
					elem = $( "#id_kabupaten" )
					make_disabled(elem, true)
				}
			})
		},
		error: function(data) {                
			toast_server_error()
		}
	});
}

function load_kabupaten(id_provinsi){
	csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	$( "#id_kabupaten_chosen" ).mLoading();
	$( "#id_kabupaten_chosen .loadmask-msg" ).css('top', '2px')
	$.ajax({ // create an AJAX call...
		data: { csrfmiddlewaretoken: csrf_token, provinsi: id_provinsi }, // get the form data
		type: 'POST', // GET or POST
		// url: '{% url 'admin:option_kabupaten' %}',
		url: __base_url__+'/admin/master/kabupaten/option/',
		success: function(response) { // on success..
			elem = $( "#id_kabupaten" )
			elem.html(response);
			make_disabled(elem, false)
			$( "#id_kabupaten_chosen" ).mLoading('hide');
			$( "#id_kabupaten" ).change(function(){
				$this = $(this)
				id_kabupaten = $(this).val()
				if(id_kabupaten.length > 0){
					load_kecamatan(id_kabupaten)
				}else{
					elem = $( "#id_kecamatan" )
					make_disabled(elem, true)
				}
			})
		},
		error: function(data) {                
			toast_server_error()
		}
	});
}
function load_kecamatan(id_kabupaten){
	csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	$( "#id_kecamatan_chosen" ).mLoading();
	$( "#id_kecamatan_chosen .loadmask-msg" ).css('top', '2px')
	$.ajax({ // create an AJAX call...
		data: { csrfmiddlewaretoken: csrf_token, kabupaten: id_kabupaten }, // get the form data
		type: 'POST', // GET or POST
		// url: '{% url 'admin:option_kecamatan' %}', // the file to call
		url: __base_url__+'/admin/master/kecamatan/option/',
		success: function(response) { // on success..
			elem = $( "#id_kecamatan" )
			elem.html(response);
			make_disabled(elem, false)
			$( "#id_kecamatan_chosen" ).mLoading('hide');
			$( "#id_kecamatan" ).change(function(){
				$this = $(this)
				
				id_kecamatan = $(this).val()
				if(id_kecamatan.length > 0){
					load_desa(id_kecamatan)
				}else{
					elem = $( "#id_desa" )
					make_disabled(elem, true)
				}
			})
		},
		error: function(data) {                
			toast_server_error()
		}
	});
}
function load_desa(id_kecamatan){
	csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	$( "#id_desa_chosen" ).mLoading();
	$( "#id_desa_chosen .loadmask-msg" ).css('top', '2px')
	$.ajax({ // create an AJAX call...
		data: { csrfmiddlewaretoken: csrf_token, kecamatan: id_kecamatan }, // get the form data
		type: 'POST', // GET or POST
		// url: '{% url 'admin:option_desa' %}', // the file to call
		url: __base_url__+'/admin/master/desa/option/',
		success: function(response) { // on success..
			elem = $( "#id_desa" )
			elem.html(response);
			make_disabled(elem, false)
			$( "#id_desa_chosen" ).mLoading('hide');
			$( "#id_desa" ).change(function(){
				$this = $(this)
			})
		},
		error: function(data) {                
			toast_server_error()
		}
	});
}

$('#profile-edit').fadeOut()

document.querySelector('#edit-profile-button').onclick = function(){
	$('#profile-show').fadeOut()
	$('#profile-edit').fadeIn()
}

document.querySelector('#batal').onclick = function(){
	$('#profile-edit').fadeOut()
	$('#profile-show').fadeIn()
}


$(window).load(function(){
	$(function () {

		'use strict';

		var console = window.console || { log: function () {} },
				$alert = $('.docs-alert'),
				$message = $alert.find('.message'),
				showMessage = function (message, type) {
					$message.text(message);

					if (type) {
						$message.addClass(type);
					}

					$alert.fadeIn();

					setTimeout(function () {
						$alert.fadeOut();
					}, 3000);
				};

		// Demo
		// -------------------------------------------------------------------------

		(function () {
			var $image = $('.img-container > img'),
					$dataX = $('#dataX'),
					$dataY = $('#dataY'),
					$dataHeight = $('#dataHeight'),
					$dataWidth = $('#dataWidth'),
					$dataRotate = $('#dataRotate'),
					options = {
						// data: {
						//   x: 420,
						//   y: 60,
						//   width: 640,
						//   height: 360
						// },
						// strict: false,
						// responsive: false,
						// checkImageOrigin: false

						// modal: false,
						// guides: false,
						// highlight: false,
						// background: false,

						// autoCrop: false,
						// autoCropArea: 0.5,
						// dragCrop: false,
						// movable: false,
						// resizable: false,
						// rotatable: false,
						// zoomable: false,
						// touchDragZoom: false,
						// mouseWheelZoom: false,

						// minCanvasWidth: 320,
						// minCanvasHeight: 180,
						// minCropBoxWidth: 160,
						// minCropBoxHeight: 90,
						// minContainerWidth: 320,
						// minContainerHeight: 180,

						// build: null,
						// built: null,
						// dragstart: null,
						// dragmove: null,
						// dragend: null,
						// zoomin: null,
						// zoomout: null,

						aspectRatio: 1 / 1,
						preview: '.img-preview',
						crop: function (data) {
							$dataX.val(Math.round(data.x));
							$dataY.val(Math.round(data.y));
							$dataHeight.val(Math.round(data.height));
							$dataWidth.val(Math.round(data.width));
							$dataRotate.val(Math.round(data.rotate));
						}
					};

			$image.on({
				'build.cropper': function (e) {
					console.log(e.type);
				},
				'built.cropper': function (e) {
					console.log(e.type);
				},
				'dragstart.cropper': function (e) {
					console.log(e.type, e.dragType);
				},
				'dragmove.cropper': function (e) {
					console.log(e.type, e.dragType);
				},
				'dragend.cropper': function (e) {
					console.log(e.type, e.dragType);
				},
				'zoomin.cropper': function (e) {
					console.log(e.type);
				},
				'zoomout.cropper': function (e) {
					console.log(e.type);
				}
			}).cropper(options);


			// Methods
			$(document.body).on('click', '[data-method]', function () {
				var data = $(this).data(),
						$target,
						result;

				if (data.method) {
					data = $.extend({}, data); // Clone a new one

					if (typeof data.target !== 'undefined') {
						$target = $(data.target);

						if (typeof data.option === 'undefined') {
							try {
								data.option = JSON.parse($target.val());
							} catch (e) {
								console.log(e.message);
							}
						}
					}

					result = $image.cropper(data.method, data.option);

					if (data.method === 'getCroppedCanvas') {
						$('#getCroppedCanvasModal').modal().find('.modal-body').html(result);
					}

					if ($.isPlainObject(result) && $target) {
						try {
							$target.val(JSON.stringify(result));
						} catch (e) {
							console.log(e.message);
						}
					}

				}
			}).on('keydown', function (e) {

				switch (e.which) {
					case 37:
						e.preventDefault();
						$image.cropper('move', -1, 0);
						break;

					case 38:
						e.preventDefault();
						$image.cropper('move', 0, -1);
						break;

					case 39:
						e.preventDefault();
						$image.cropper('move', 1, 0);
						break;

					case 40:
						e.preventDefault();
						$image.cropper('move', 0, 1);
						break;
				}

			});


			// Import image
			var $inputImage = $('#inputImage'),
					URL = window.URL || window.webkitURL,
					blobURL;

			if (URL) {
				$inputImage.change(function () {
					var files = this.files,
							file;

					if (files && files.length) {
						file = files[0];

						if (/^image\/\w+$/.test(file.type)) {
							blobURL = URL.createObjectURL(file);
							$image.one('built.cropper', function () {
								URL.revokeObjectURL(blobURL); // Revoke when load complete
							}).cropper('reset').cropper('replace', blobURL);
							$inputImage.val('');
						} else {
							showMessage('Please choose an image file.');
						}
					}
				});
			} else {
				$inputImage.parent().remove();
			}


			// Options
			$('.docs-options :checkbox').on('change', function () {
				var $this = $(this);

				options[$this.val()] = $this.prop('checked');
				$image.cropper('destroy').cropper(options);
			});


			// Tooltips
			$('[data-toggle="tooltip"]').tooltip();

		}());

	});
});