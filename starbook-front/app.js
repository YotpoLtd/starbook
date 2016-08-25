angular.module('myApp', ['ngCookies']);
angular.element(document).ready(function() {

    angular.module('myApp')
        .controller('myCtrl', ['$scope', '$http', 'elastic', '$timeout', function ($scope, $http, elastic, $timeout) {
            $scope.search = '';

            $scope.textChanged = function (text) {
                if (!!this.search) {
                    $scope.showTable = true;
                    if (this.search.length > 1) {

                        var nohash = this.search.replace('#','');
                        var term = nohash.replace(/ /g,"*") + "*";

                        $scope.names = elastic.get(term, function (data) {

                            var names = [];

                            angular.forEach(data.hits.hits, function(value, key) {
                                names.push(value._source.name)
                            });
                            console.log(names);
                            $scope.names = names;
                        });
                    }
                } else {
                    $scope.showTable = false;
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

            $scope.showTable = false;

        }])
        .config(function ($httpProvider) {
            delete $httpProvider.defaults.headers.common['X-Requested-With'];
        });

    angular.bootstrap(document,['myApp']);

});