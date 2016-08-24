angular.module('myApp')
  .controller('mainCtrl', ['$scope', '$http', 'elastic', 'ENV', '$timeout', '$window', '$cookies',
    function($scope, $http, elastic, ENV, $timeout, $window, $cookies) {
      var auth2;
      var self = this;
      var starbook_token = 'starbook-token';

      $scope.search = '';

      self.auth = false;

      gapi.load('auth2', function() {
        self.auth = !ENV.SEND_COOKIES || $cookies.get(starbook_token);

        if (ENV.SEND_COOKIES) {
          auth2 = gapi.auth2.init({
            client_id: ENV.GOOGLE_SIGN_IN_CLIENT_ID,
            cookiepolicy: 'single_host_origin'
            // Request scopes in addition to 'profile' and 'email'
            //scope: 'additional_scope'
          });

          auth2.then(function() {
            if (auth2.isSignedIn.get()) {
              elastic.tree().success(function(response) {
                self.email = auth2.currentUser.get().getBasicProfile().getEmail();
                populateGraph(response);
              }).error(function() {
                //self.signIn();
              });
            } else {
              //self.signIn();
            }
          })
        } else {
          elastic.tree().success(function(response) {
            populateGraph(response);
          })
        }


      });

      self.signIn = function() {
        auth2.signIn().then(function() {
          $timeout(function() {
            self.auth = true;
            var token = auth2.currentUser.get().getAuthResponse().id_token;
            console.log(token);
            $cookies.put(starbook_token, token);
            $window.location.reload();
          });
        });
      };

      self.signOut = function() {
        auth2.signOut().then(function() {
          $timeout(function() {
            self.auth = false;
            console.log('User signed out.');
            $cookies.remove(starbook_token);
            $window.location.reload();
          });
        });
      };

      self.meClicked = function() {
        if (self.email) {
          globalVar.updateBy({email: self.email});
        }
      }

    }]);
