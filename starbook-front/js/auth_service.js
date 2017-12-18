angular.module('myApp')
  .factory('authService', ['$timeout', '$cookies', '$q', 'ENV',
    function($timeout, $cookies, $q, ENV) {
      var starbook_token = 'starbook-token';

      function saveToken(auth2) {
        var token = auth2.currentUser.get().getAuthResponse().id_token;
        console.log(token);
        $cookies.put(starbook_token, token);
      }

      return {
        saveToken: saveToken,
        retry: function() {
          var deferred = $q.defer();
          var afterLoad = function() {
            var auth2 = gapi.auth2.getAuthInstance();
            if (!auth2) {
              auth2 = gapi.auth2.init({
                client_id: ENV.GOOGLE_SIGN_IN_CLIENT_ID,
                cookiepolicy: 'single_host_origin'
                // Request scopes in addition to 'profile' and 'email'
                //scope: 'additional_scope'
              });
            }

            auth2.then(function() {
              $timeout(function() {
                var auth = auth2.isSignedIn.get();
                if (auth) {
                  saveToken(auth2);
                  deferred.resolve();
                } else {
                  deferred.reject();
                }
              });
            })
          };
          if (gapi.auth2) {
            afterLoad();
          } else {
            gapi.load('auth2', afterLoad);
          }
          return deferred.promise;
        }
      }
    }]);
