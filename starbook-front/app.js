angular.module('myApp', ['ngCookies','ngMaterial', 'ngMessages', 'material.svgAssetsCache']);
angular.element(document).ready(function() {

    angular.module('myApp')
        .controller('myCtrl', ['$scope', '$http', 'elastic', '$timeout', '$mdDialog', function ($scope, $http, elastic, $timeout, $mdDialog) {
            $scope.search = '';

            $scope.textChanged = function () {
                $scope.showTable = false;
                if ($scope.search.length > 0) {
                    // For example if search = ' #abc #adf  sw45   asdfg  '
                    // It will be replaces with 'abc* adf* sw45* asdfg*'
                    var term = $scope.search.replace(/\W/g, ' ').trim().split(/\s+/).join('* ') + '*';
                    elastic.get(term, function (data) {
                        var names = [];
                        angular.forEach(data.hits.hits, function(value, key) {
                            names.push(value._source.name)
                        });
                        console.log(names);
                        $scope.names = names;
                        $scope.showTable = names.length > 0;
                    });
                }
            };

            $scope.onLeaveSearch = function () {
                $timeout(function() {
                    $scope.showTable = false;
                }, 500);
            };

            $scope.nameClicked =  function (name) {
                globalVar.updateBy({name: name});
            };

            function updateUserDetails(email, currentList, additionList, key, callback) {
                currentList = additionList.concat(currentList);
                currentList = $.map(currentList, function(name){
                    return name.replace ? name.replace(/\s/g, '') : undefined;
                });

                var data = { email: email}
                data[key] = currentList;

                elastic.update(data).success(function (response) {
                    console.log(response);
                    if (callback){
                        callback();
                    }
                }).error(function (error) {
                    console.log(error);
                });
            }

            $scope.addSkill =  function (name) {
                var confirm = $mdDialog.prompt()
                    .title('What\'s the name of your skill?')
                    .placeholder('Skill name')
                    .ariaLabel('Skill name')
                    .ok('Submit')
                    .cancel('Cancel');
                $mdDialog.show(confirm).then(function(result) {
                    var email = globalVar.currentUser.email;
                    var expertise = globalVar.currentUser.expertise || [];
                    var additionalExpertises = result.split(',');
                    updateUserDetails(email, expertise, additionalExpertises, 'expertise', function () {
                        angular.forEach(additionalExpertises, function(value, key) {
                            globalVar.currentUser.expertise.push(value);
                            var skillSpan = angular.element('<span class="user-skill">' + value + '<i style="display: none" class="delete-skill-x fa fa-times-circle"></i></span>');
                            skillSpan.data('skill-name', value);
                            skillSpan.data('key', 'expertise');
                            skillSpan.click(globalVar.deleteSkill);
                            angular.element('.user-skills').append(skillSpan);
                        });
                    });
                }, function() {
                    // user canceled
                });
            };

            $scope.addHobby =  function (name) {
                var confirm = $mdDialog.prompt()
                    .title('What\'s the name of your hobby?')
                    .placeholder('Hobbie name')
                    .ariaLabel('Skill name')
                    .ok('Submit')
                    .cancel('Cancel');
                $mdDialog.show(confirm).then(function(result) {
                    var email = globalVar.currentUser.email;
                    var hobbies = globalVar.currentUser.hobbies || [];
                    var additionalHobbies = result.split(',');
                    updateUserDetails(email, hobbies, additionalHobbies, 'hobbies', function () {
                        angular.forEach(additionalHobbies, function(value, key) {
                            globalVar.currentUser.hobbies.push(value);
                            var hobbySpan = angular.element('<span class="user-skill">' + value + '<i style="display: none" class="delete-hobby-x fa fa-times-circle"></i></span>');
                            hobbySpan.data('skill-name', value);
                            hobbySpan.data('key', 'hobbies');
                            hobbySpan.click(globalVar.deleteSkill);
                            angular.element('.user-hobbies').append(hobbySpan);
                        });
                    });
                }, function() {
                    // user canceled
                });
            };

            $scope.showTable = false;

        }])
        .config(function ($httpProvider) {
            delete $httpProvider.defaults.headers.common['X-Requested-With'];
        });

    angular.bootstrap(document,['myApp']);

});