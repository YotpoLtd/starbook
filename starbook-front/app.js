angular.module('myApp', ['ngCookies', 'ngMaterial', 'ngMessages', 'material.svgAssetsCache']);

angular.element(document).ready(function() {

  angular.module('myApp')
    .controller('myCtrl', ['$scope', '$http', 'api', '$timeout', '$mdDialog', '$sce',
      function($scope, $http, api, $timeout, $mdDialog, $sce) {
        var self = this;

        self.search = '';

        self.textChanged = function() {
          self.showTable = false;
          if (self.search.length > 0) {
            // For example if search = ' #abc #adf  sw45   asdfg  '
            // It will be replaces with 'abc* adf* sw45* asdfg*'
            var term = self.search.replace(/\W/g, ' ').trim().split(/\s+/).join('* ') + '*';
            api.get(term, function(data) {
              self.people = data && data.hits && data.hits.hits.map(function(person) {
                  person.name = $sce.trustAsHtml((person.highlight && person.highlight.name && person.highlight.name[0]) || person._source.name);
                  var keys = $.grep(Object.keys(person.highlight), function(h) {
                    return h !== 'name'
                  });
                  person.highlights = keys.map(function(key) {
                    return {
                      key: key,
                      value: $sce.trustAsHtml(person.highlight[key][0])
                    }
                  });
                  return person;
                });
              self.showTable = self.people && self.people.length > 0;
            });
          }
        };

        self.onLeaveSearch = function() {
          $timeout(function() {
            self.showTable = false;
          }, 500);
        };

        self.personClicked = function(person) {
          var name = person._source.name;
          globalVar.updateBy({ name: name });
          self.onLeaveSearch();
        };

        function normalizeListOfStrings(listOfStrings) {
          return $.map(listOfStrings, function(str) {
            return str.replace ? str.replace(/\s+/g, ' ').trim() : undefined;
          })
        }

        function updateUserDetails(email, currentList, additionList, key, callback) {
          currentList = additionList.concat(currentList);

          var data = { email: email };
          data[key] = currentList;

          api.update(data).success(function() {
            if (callback) {
              callback();
            }
          }).error(function(error) {
            console.log(error);
          });
        }

        $scope.addSkill = function(name) {
          var confirm = $mdDialog.prompt()
            .title('What\'s the name of your skill?')
            .placeholder('Skill name')
            .ariaLabel('Skill name')
            .ok('Submit')
            .cancel('Cancel');
          $mdDialog.show(confirm).then(function(result) {
            var email = globalVar.currentUser.email;
            globalVar.currentUser.expertise = globalVar.currentUser.expertise || [];
            var additionalExpertises = normalizeListOfStrings(result.split(','));
            updateUserDetails(email, globalVar.currentUser.expertise, additionalExpertises, 'expertise', function() {
              angular.forEach(additionalExpertises, function(value, key) {
                globalVar.currentUser.expertise.push(value);
                var skillSpan = angular.element('<span class="user-skill">' + value + '<i style="display: none" class="delete-skill-x fa fa-times-circle"></i></span>');
                skillSpan.data('skill-name', value);
                skillSpan.data('key', 'expertise');
                angular.element('.user-skills').append(skillSpan);
              });
            });
          }, function() {
            // user canceled
          });
        };

        self.setSearch = function(ev) {
          var el = $(ev.toElement);
          if (el.hasClass('user-skill')) {
            self.search = el.text();
            self.textChanged();
          }
        };

        $scope.addHobby = function(name) {
          var confirm = $mdDialog.prompt()
            .title('What\'s the name of your hobby?')
            .placeholder('Hobbie name')
            .ariaLabel('Skill name')
            .ok('Submit')
            .cancel('Cancel');
          $mdDialog.show(confirm).then(function(result) {
            var email = globalVar.currentUser.email;
            globalVar.currentUser.hobbies = globalVar.currentUser.hobbies || [];
            var additionalHobbies = normalizeListOfStrings(result.split(','));
            updateUserDetails(email, globalVar.currentUser.hobbies, additionalHobbies, 'hobbies', function() {
              angular.forEach(additionalHobbies, function(value, key) {
                globalVar.currentUser.hobbies.push(value);
                var hobbySpan = angular.element('<span class="user-skill">' + value + '<i style="display: none" class="delete-hobby-x fa fa-times-circle"></i></span>');
                hobbySpan.data('skill-name', value);
                hobbySpan.data('key', 'hobbies');
                angular.element('.user-hobbies').append(hobbySpan);
              });
            });
          }, function() {
            // user canceled
          });
        };

        self.showTable = false;

        $scope.isAdmin = function() {
          return this.$parent.mainCtrl.role ? this.$parent.mainCtrl.role.admin : false;
        }

        $scope.showConfirm = function(ev) {
          var confirm = $mdDialog.confirm()
            .title('Delete ' + globalVar.currentUser.name + '. Are you sure?')
            .textContent('User details cannot be restored after deletion.')
            .targetEvent(ev)
            .ok('Yes')
            .cancel('Cancel');
          $mdDialog.show(confirm).then(function() {
            removePerson();
          }, function() {
            // user deletion cancelled
          });
        };

        function removePerson() {
          var email_to_remove = globalVar.currentUser.email;
          api.remove_person(email_to_remove, function(data) {
            console.log(data);
          });
          location.reload();
        }

      }])
    .config(function($httpProvider) {
      delete $httpProvider.defaults.headers.common['X-Requested-With'];
    });

  angular.bootstrap(document, ['myApp']);

});