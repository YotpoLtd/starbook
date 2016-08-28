angular.module('myApp', ['ngCookies']);
angular.element(document).ready(function() {

    angular.module('myApp')
        .controller('myCtrl', ['$scope', '$http', 'elastic', '$timeout', function ($scope, $http, elastic, $timeout) {
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

            $scope.showTable = false;

        }])
        .config(function ($httpProvider) {
            delete $httpProvider.defaults.headers.common['X-Requested-With'];
        });

    angular.bootstrap(document,['myApp']);

});