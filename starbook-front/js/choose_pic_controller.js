angular.module('myApp')
  .controller('ChoosePicController', ['$scope', '$mdDialog', '$timeout', function($scope, $mdDialog, $timeout) {
    var self = this;
    this.pics = [
      {
        value: 'google',
        label: 'Google'
      },
      {
        value: 'facebook',
        label: 'Facebook'
      }
    ];

    this.image = {
      google: window.globalVar.logged_image
    };

    $timeout(function () {
      FB.XFBML.parse();
      FB.getLoginStatus(function(response) {
        handleFacebookResponse(response);
      });

    });

    self.choosePic = function() {
      if (self.pic === 'facebook') {
        FB.getLoginStatus(function(response) {
          if (!handleFacebookResponse(response)) {
            FB.login(function(response) {
              handleFacebookResponse(response);
            });
          }
        });
      }
    };

    function handleFacebookResponse(response) {
      if (response.status === 'connected') {
        FB.api('/me/picture?width=96&height=96', function(response) {
          $timeout(function() {
            self.image.facebook = response.data && response.data.url;
          });
        });
        return true;
      }
      return false;
    }



    this.ok = function() {
      if ($scope.form.$valid) {
        $mdDialog.hide(self.image[self.pic]);
      }
    }
  }]);
