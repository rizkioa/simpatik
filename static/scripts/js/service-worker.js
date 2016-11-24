var dataCacheName = '[javascript-css]-v1';
var cacheName = '[javascript-css]-v1';
var PATH = '';
var filesToCache = [
   // IMG
   PATH + '/static/images/kabkediri.png',
   PATH + '/static/images/SIMPATIK.ico',
   PATH + '/static/images/alur.png',

   // JS
   PATH + '/static/scripts/js/vendor/modernizr/modernizr-2.8.3-respond-1.4.2.min.js',
   PATH + '/static/scripts/js/vendor/wow/wow.js',
   PATH + '/static/scripts/js/vendor/jquery/jquery-1.11.2.min.js',
   PATH + '/static/scripts/js/vendor/bootstrap/bootstrap.min.js',
   PATH + '/static/scripts/js/vendor/jRespond/jRespond.min.js',
   PATH + '/static/scripts/js/vendor/slimscroll/jquery.slimscroll.min.js',
   PATH + '/static/scripts/js/vendor/animsition/js/jquery.animsition.min.js',
   PATH + '/static/scripts/js/mainfront.js',
   // CSS
   PATH + '/static/styles/css/main_site.css',
   PATH + '/static/styles/css/vendor/bootstrap.min.css',
   PATH + '/static/styles/css/vendor/animate.css',
   PATH + '/static/styles/css/vendor/font-awesome.min.css',
   PATH + '/static/scripts/js/vendor/animsition/css/animsition.min.css',
   PATH + '/static/styles/css/mainfront.css',
   PATH + '/static/styles/css/mobile-frontend.css',
   PATH + '/static/styles/css/vendor/color-background.css',

   // PAGES
   PATH + '',
   PATH + '/index.html',
   PATH + '/layanan/',
   PATH + '/layanan/siup',

];
self.addEventListener( 'install', function( e ) {
   console.log( '[ServiceWorker] Install' );
   e.waitUntil( caches.open( cacheName ).then( function( cache ) {
      console.log( '[ServiceWorker] Caching app shell' );
      return cache.addAll( filesToCache );
   } ) );
} );
self.addEventListener( 'activate', function( e ) {
   console.log( '[ServiceWorker] Activate' );
   e.waitUntil( caches.keys().then( function( keyList ) {
      return Promise.all( keyList.map( function( key ) {
         if ( key !== cacheName ) {
            console.log( '[ServiceWorker] Removing old cache', key );
            return caches.delete( key );
         }
      } ) );
   } ) );
} );
self.addEventListener( 'fetch', function( e ) {
   console.log( '[ServiceWorker] Fetch', e.request.url );
   if ( e.request.url.indexOf( dataUrl ) === 0 ) {
      e.respondWith( fetch( e.request ).then( function( response ) {
         return caches.open( dataCacheName ).then( function( cache ) {
            cache.put( e.request.url, response.clone() );
            console.log( '[ServiceWorker] Fetched&Cached Data' );
            return response;
         } );
      } ) );
   } else {
      e.respondWith( caches.match( e.request ).then( function( response ) {
         return response || fetch( e.request );
      } ) );
   }
} );