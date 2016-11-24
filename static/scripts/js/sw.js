self.addEventListener('install', e => {
  e.waitUntil(
    caches.open('simpatik').then(cache => {
      return cache.addAll([
        '/',
        // IMG
        '/static/images/kabkediri.png',
        '/static/images/SIMPATIK.ico',
        '/static/images/alur.png',
        // JS
        '/static/scripts/js/vendor/modernizr/modernizr-2.8.3-respond-1.4.2.min.js',
        '/static/scripts/js/vendor/wow/wow.js',
        '/static/scripts/js/vendor/jquery/jquery-1.11.2.min.js',
        '/static/scripts/js/vendor/bootstrap/bootstrap.min.js',
        '/static/scripts/js/vendor/jRespond/jRespond.min.js',
        '/static/scripts/js/vendor/slimscroll/jquery.slimscroll.min.js',
        '/static/scripts/js/vendor/animsition/js/jquery.animsition.min.js',
        '/static/scripts/js/mainfront.js',
        '/static/scripts/js/vendor/chosen/chosen.jquery.js',
        '/static/scripts/js/vendor/alert/sweetalert-dev.js',
        '/static/scripts/js/vendor/parsley/parsley.js',
        '/static/scripts/js/vendor/form-wizard/jquery.bootstrap.wizard.min.js',
        '/static/scripts/js/vendor/toastr/toastr.min.js',
        '/static/scripts/js/vendor/loadmask/jquery.loadmask.js',
        '/static/scripts/js/vendor/filestyle/bootstrap-filestyle.min.js',
        '/static/scripts/js/vendor/daterangepicker/moment.js',
        '/static/scripts/js/vendor/datetimepicker/js/bootstrap-datetimepicker.min.js',
        '/static/scripts/js/vendor/validation/jquery.maskedinput.js',
        '/static/scripts/js/vendor/jquery/jquery.cookie.js',
        '/static/scripts/js/vendor/alert/sweetalert-dev.js',
        '/static/scripts/js/mloading/jquery.mloading.js',
        '/static/scripts/js/vendor/jquery/jquery.form.js',
        '/static/scripts/js/vendor/jquery/jquery.cookie.js',
        '/static/scripts/js/formAjax/form_ajax_siup.js',
        '/static/scripts/js/jquery.maskMoney.min.js',
        '/static/scripts/js/vendor/touchspin/jquery.bootstrap-touchspin.min.js'


        // CSS
        '/static/scripts/js/vendor/chosen/chosen.min.css',
        '/static/scripts/js/vendor/toastr/toastr.min.css',
        '/static/scripts/js/vendor/loadmask/jquery.loadmask.css',
        '/static/scripts/js/vendor/datetimepicker/css/bootstrap-datetimepicker.min.css',
        '/static/scripts/js/vendor/alert/sweetalert.css',
        '/static/styles/css/main_site.css',
        '/static/styles/css/vendor/bootstrap.min.css',
        '/static/styles/css/vendor/animate.css',
        '/static/styles/css/vendor/font-awesome.min.css',
        '/static/scripts/js/vendor/animsition/css/animsition.min.css',
        '/static/styles/css/mainfront.css',
        '/static/styles/css/mobile-frontend.css',
        '/static/styles/css/vendor/color-background.css',
        '/static/scripts/js/mloading/jquery.mloading.css'
        // PAGES
        '/layanan/',
        '/layanan/siup',
        '/layanan/siup/formulir'

      ])
      .then(() => self.skipWaiting());
    })
  )
});

self.addEventListener('activate',  event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});