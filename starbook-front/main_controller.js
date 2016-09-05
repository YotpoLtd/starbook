angular.module('myApp')
  .controller('mainCtrl', ['$scope', '$http', 'api', 'ENV', '$timeout', '$window', '$cookies', '$mdDialog',
    function($scope, $http, api, ENV, $timeout, $window, $cookies, $mdDialog) {
      var auth2;
      var self = this;
      var starbook_token = 'starbook-token';

      $scope.search = '';

      self.auth = true;

      gapi.load('auth2', function() {

        if (ENV.SEND_COOKIES) {
          auth2 = gapi.auth2.init({
            client_id: ENV.GOOGLE_SIGN_IN_CLIENT_ID,
            cookiepolicy: 'single_host_origin'
            // Request scopes in addition to 'profile' and 'email'
            //scope: 'additional_scope'
          });

          auth2.then(function() {
            $timeout(function() {
              self.auth = auth2.isSignedIn.get();
              if (self.auth) {
                window.globalVar = window.globalVar || {};
                var basicProfile = auth2.currentUser.get().getBasicProfile();
                window.globalVar.looged_user_email = basicProfile.getEmail();
                window.globalVar.logged_image = basicProfile.getImageUrl();
                api.tree().success(function(response) {
                  self.email = auth2.currentUser.get().getBasicProfile().getEmail();
                  api.get_role().success(function(role) {
                    self.role = role;
                  });
                  populateGraph(response);
                }).error(function() {
                  self.auth = false;
                });
              }
            });
          })
        } else {
          api.tree().success(function(response) {
            populateGraph(response);
          })
        }


      });

      self.signIn = function() {
        auth2.signIn().then(function() {
          $timeout(function() {
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
      };

      self.editTitle = function () {
        var newTitle;
        var confirm = $mdDialog.prompt()
          .title('Edit Title')
          .initialValue(window.globalVar.currentUser.title)
          .placeholder('Title')
          .ok('Submit')
          .cancel('Cancel');
        $mdDialog.show(confirm).then(function(result) {
          var email = window.globalVar.currentUser.email;
          newTitle = result;
          return api.update({email: email, title: result});
        }).then(function() {
          window.globalVar.currentUser.title = newTitle;
          var userTitle = document.getElementsByClassName("user-title")[0];
          userTitle.textContent = newTitle;
        }, function() {
          // user canceled
        });
      };

      self.editPhone = function() {
        if (globalVar.currentUser.email !== globalVar.looged_user_email) {
          return;
        }
        var newPhone;
        var confirm = $mdDialog.prompt()
          .title('Edit Phone')
          .initialValue(window.globalVar.currentUser.phone)
          .placeholder('Phone')
          .ok('Submit')
          .cancel('Cancel');
        $mdDialog.show(confirm).then(function(result) {
          var email = window.globalVar.currentUser.email;
          newPhone = result;
          return api.update({email: email, phone: result});
        }).then(function() {
          window.globalVar.currentUser.phone = newPhone;
          var userPhone = document.getElementsByClassName("user-phone")[0];
          userPhone.textContent = newPhone;
        }, function() {
          // user canceled
        });
      }

    }]);
