// lokasi = document.createElement("a");
// lokasi.href = location.href;
// window.__base_url__ = lokasi.protocol+"//"+lokasi.host;
// var __base_url__ = 'http://simpatik.kedirikab.go.id';
// self.addEventListener('install', e => {
//   e.waitUntil(
//     caches.open('simpatik').then(cache => {
//       return cache.addAll([
//         '/',
//         // IMG
//         '/static/images/kabkediri.png',
//         '/static/images/SIMPATIK.ico',
//         '/static/images/alur.png',
//         // JS
//         '/static/scripts/js/vendor/modernizr/modernizr-2.8.3-respond-1.4.2.min.js',
//         '/static/scripts/js/vendor/wow/wow.js',
//         '/static/scripts/js/vendor/jquery/jquery-2.1.1.min.js',
//         '/static/scripts/js/vendor/bootstrap/bootstrap.min.js',
//         '/static/scripts/js/vendor/jRespond/jRespond.min.js',
//         '/static/scripts/js/vendor/slimscroll/jquery.slimscroll.min.js',
//         '/static/scripts/js/vendor/animsition/js/jquery.animsition.min.js',
//         '/static/scripts/js/mainfront.js',
//         '/static/scripts/js/vendor/chosen/chosen.jquery.js',
//         '/static/scripts/js/vendor/alert/sweetalert-dev.js',
//         '/static/scripts/js/vendor/parsley/parsley.js',
//         '/static/scripts/js/vendor/form-wizard/jquery.bootstrap.wizard.min.js',
//         '/static/scripts/js/vendor/toastr/toastr.min.js',
//         '/static/scripts/js/vendor/loadmask/jquery.loadmask.js',
//         '/static/scripts/js/vendor/filestyle/bootstrap-filestyle.min.js',
//         '/static/scripts/js/vendor/daterangepicker/moment.js',
//         '/static/scripts/js/vendor/datetimepicker/js/bootstrap-datetimepicker.min.js',
//         '/static/scripts/js/vendor/validation/jquery.maskedinput.js',
//         '/static/scripts/js/vendor/jquery/jquery.cookie.js',
//         '/static/scripts/js/vendor/alert/sweetalert-dev.js',
//         '/static/scripts/js/mloading/jquery.mloading.js',
//         '/static/scripts/js/vendor/jquery/jquery.form.js',
//         '/static/scripts/js/vendor/jquery/jquery.cookie.js',
//         '/static/scripts/js/formAjax/form_ajax_siup.js',
//         '/static/scripts/js/formAjax/form_ajax_reklame.js',
//         '/static/scripts/js/jquery.maskMoney.min.js',
//         '/static/scripts/js/vendor/touchspin/jquery.bootstrap-touchspin.min.js',


//         // CSS
//         '/static/scripts/js/vendor/chosen/chosen.min.css',
//         '/static/scripts/js/vendor/toastr/toastr.min.css',
//         '/static/scripts/js/vendor/loadmask/jquery.loadmask.css',
//         '/static/scripts/js/vendor/datetimepicker/css/bootstrap-datetimepicker.min.css',
//         '/static/scripts/js/vendor/alert/sweetalert.css',
//         '/static/styles/css/main_site.css',
//         '/static/styles/css/vendor/bootstrap.min.css',
//         '/static/styles/css/vendor/animate.css',
//         '/static/styles/css/vendor/font-awesome.min.css',
//         '/static/scripts/js/vendor/animsition/css/animsition.min.css',
//         '/static/styles/css/mainfront.css',
//         '/static/styles/css/mobile-frontend.css',
//         '/static/styles/css/vendor/color-background.css',
//         '/static/scripts/js/mloading/jquery.mloading.css',
//         'http://fonts.googleapis.com/css?family=Dosis:300,700|Ubuntu+Mono|Lato:300,400,700,300italic,400italic&subset=latin,latin-ext',
//         // PAGES
//         '/layanan/',
//         '/layanan/siup',
//         '/layanan/siup/formulir'

//       ])
//       .then(() => self.skipWaiting());
//     })
//   )
// });

// self.addEventListener('activate',  event => {
//   event.waitUntil(self.clients.claim());
// });

// self.addEventListener('fetch', event => {
//   event.respondWith(
//     caches.match(event.request).then(response => {
//       return response || fetch(event.request);
//     })
//   );
// });

// Set a name for the current cache
var cacheName = 'v1'; 

// Default files to always cache
var cacheFiles = [  
    '/',
    // IMG
    '/static/images/kabkediri.png',
    '/static/images/SIMPATIK.ico',
    '/static/images/alur.png',
    // JS
    '/static/scripts/js/vendor/modernizr/modernizr-2.8.3-respond-1.4.2.min.js',
    '/static/scripts/js/vendor/wow/wow.js',
    '/static/scripts/js/vendor/jquery/jquery-2.1.1.min.js',
    '/static/scripts/js/vendor/bootstrap/bootstrap.min.js',
    '/static/scripts/js/vendor/jRespond/jRespond.min.js',
    '/static/scripts/js/vendor/slimscroll/jquery.slimscroll.min.js',
    '/static/scripts/js/vendor/animsition/js/jquery.animsition.min.js',
    '/static/scripts/js/mainfront.js',
    '/static/scripts/js/vendor/chosen/chosen.jquery.js',
    '/static/scripts/js/vendor/alert/sweetalert-dev.js',
    '/static/scripts/js/vendor/parsley/parsley.js',
    '/static/scripts/js/vendor/form-wizard/jquery.bootstrap.wizard.min.js',
    // '/static/scripts/js/vendor/toastr/toastr.min.js',
    // '/static/scripts/js/vendor/loadmask/jquery.loadmask.js',
    // '/static/scripts/js/vendor/filestyle/bootstrap-filestyle.min.js',
    // '/static/scripts/js/vendor/daterangepicker/moment.js',
    // '/static/scripts/js/vendor/datetimepicker/js/bootstrap-datetimepicker.min.js',
    // '/static/scripts/js/vendor/validation/jquery.maskedinput.js',
    // '/static/scripts/js/vendor/jquery/jquery.cookie.js',
    // '/static/scripts/js/vendor/alert/sweetalert-dev.js',
    // '/static/scripts/js/mloading/jquery.mloading.js',
    // '/static/scripts/js/vendor/jquery/jquery.form.js',
    // '/static/scripts/js/vendor/jquery/jquery.cookie.js',
    // '/static/scripts/js/formAjax/form_ajax_siup.js',
    // '/static/scripts/js/formAjax/form_ajax_reklame.js',
    // '/static/scripts/js/jquery.maskMoney.min.js',
    // '/static/scripts/js/vendor/touchspin/jquery.bootstrap-touchspin.min.js',


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
    '/static/scripts/js/mloading/jquery.mloading.css',
    'http://fonts.googleapis.com/css?family=Dosis:300,700|Ubuntu+Mono|Lato:300,400,700,300italic,400italic&subset=latin,latin-ext',
    // PAGES
    '/layanan/',
    '/layanan/siup',
    '/layanan/siup/formulir'
]


self.addEventListener('install', function(e) {  
    console.log('[ServiceWorker] Installed');

    // e.waitUntil Delays the event until the Promise is resolved
    e.waitUntil(

        // Open the cache
        caches.open(cacheName).then(function(cache) {

            // Add all the default files to the cache
            console.log('[ServiceWorker] Caching cacheFiles');
            return cache.addAll(cacheFiles);
        })
    ); // end e.waitUntil
});


self.addEventListener('activate', function(e) {  
    console.log('[ServiceWorker] Activated');

    e.waitUntil(

        // Get all the cache keys (cacheName)
        caches.keys().then(function(cacheNames) {
            return Promise.all(cacheNames.map(function(thisCacheName) {

                // If a cached item is saved under a previous cacheName
                if (thisCacheName !== cacheName) {

                    // Delete that cached file
                    console.log('[ServiceWorker] Removing Cached Files from Cache - ', thisCacheName);
                    return caches.delete(thisCacheName);
                }
            }));
        })
    ); // end e.waitUntil

});


self.addEventListener('fetch', function(e) {  
    console.log('[ServiceWorker] Fetch', e.request.url);

    // e.respondWidth Responds to the fetch event
    e.respondWith(

        // Check in cache for the request being made
        caches.match(e.request)


            .then(function(response) {

                // If the request is in the cache
                if ( response ) {
                    console.log("[ServiceWorker] Found in Cache", e.request.url, response);
                    // Return the cached version
                    return response;
                }

                // If the request is NOT in the cache, fetch and cache

                var requestClone = e.request.clone();
                fetch(requestClone)
                    .then(function(response) {

                        if ( !response ) {
                            console.log("[ServiceWorker] No response from fetch ")
                            return response;
                        }

                        var responseClone = response.clone();

                        //  Open the cache
                        caches.open(cacheName).then(function(cache) {

                            // Put the fetched response in the cache
                            cache.put(e.request, responseClone);
                            console.log('[ServiceWorker] New Data Cached', e.request.url);

                            // Return the response
                            return response;

                        }); // end caches.open

                    })
                    .catch(function(err) {
                        console.log('[ServiceWorker] Error Fetching & Caching New Data', err);
                    });


            }) // end caches.match(e.request)
    ); // end e.respondWith
});
