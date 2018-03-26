angular.module('myApp')
  .controller('AddPersonController', ['$scope', '$mdDialog', function($scope, $mdDialog) {
    var self = this;
    this.fields = {};

    this.ok = function() {
      if ($scope.form.$valid) {
        $mdDialog.hide(self.fields);
      }
    }
  }]);