angular.module('myApp')
  .controller('UpdatePersonController', ['$scope', '$mdDialog', function($scope, $mdDialog) {
    var self = this;
    this.person = window.globalVar.currentUser;
    this.fieldName = undefined;
    this.fieldValue = undefined;
    this.keyValue = {};
    this.possibleFields = ['boss', 'name', 'title', 'hood', 'phone'];

    this.fieldNameSelected = function() {
      self.fieldValue = window.globalVar.currentUser[self.fieldName];
    };

    this.fieldValueChanged = function() {
      self.keyValue[self.fieldName] = self.fieldValue;
    };

    this.ok = function() {
      if ($scope.form.$valid) {
        $mdDialog.hide(self.keyValue);
      }
    }
  }]);
