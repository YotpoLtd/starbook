angular.module('myApp', ['ngCookies']);
angular.element(document).ready(function(){

    //TODO - remove this
    var treeData = [
        {
            "name": "Tomer",
            "parent": "null",
            "image": "https://image1.owler.com/1406625103081.jpg",
            "children": [
                {
                    "name": "Omri",
                    "parent": "Tomer",
                    "image": "http://d1xqlf737dvrs6.cloudfront.net/people/attachments/2841/Omri.jpg?1434445241",
                    "_children": [
                        {
                            "name": "Avi",
                            "parent": "Omri",
                            "image": "https://media.licdn.com/mpr/mpr/shrinknp_200_200/AAEAAQAAAAAAAAlkAAAAJDNjNWE0M2ViLTFiMjAtNDQ2YS04YTE4LWY0MDk0NDdjZjYwMg.jpg",
                            "_children": [
                                {
                                    "name": "Vlad",
                                    "parent": "Avi",
                                    "image": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/v/t1.0-1/c52.52.654.654/s320x320/946315_10151516357822912_1008922215_n.jpg?oh=1ce2c800f2597d8d1ca1dbe9c7afecc4&oe=581C9C0F&__gda__=1481589886_56a32644ebb69dd514a518a743af9aca"
                                },
                                {
                                    "name": "Micha",
                                    "parent": "Avi",
                                    "image": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xfa1/v/t1.0-1/c44.44.552.552/s320x320/545333_10150843153544962_234301019_n.jpg?oh=bc20d3ac4ba3550d5728c48903fe0f2e&oe=585F034A&__gda__=1481407060_124858c6664c49f8ef5f79c86b2af48b"
                                },
                                {
                                    "name": "Jonny",
                                    "parent": "Avi",
                                    "image": "https://scontent-fra3-1.xx.fbcdn.net/v/t1.0-9/19824_10152646262246104_6217364817411149298_n.jpg?oh=d854826a20433fbc220101904c6964a5&oe=58583A77"
                                },
                                {
                                    "name": "Livne",
                                    "image": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xaf1/v/t1.0-1/p320x320/11694762_10153330718303726_7929876429216413920_n.jpg?oh=8ba078a98903938a6402b02c284181b9&oe=5820D5F3&__gda__=1482619240_83c38d84f90269865aa66dd58ad04990",
                                    "parent": "Avi"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Rotem",
                    "parent": "Tomer",
                    "image": "https://media.licdn.com/mpr/mpr/shrinknp_200_200/AAEAAQAAAAAAAANvAAAAJDBhNDFlZThiLTFmMDQtNGFlYy1iODQ1LWQzMDhiZmEyNDg5Nw.jpg"
                }
            ]
        }
    ];

    angular.module('myApp')
        .controller('myCtrl', ['$scope','store', '$http', 'elastic', '$timeout',function ($scope, store, $http, elastic, $timeout) {
            $scope.search = '';
            //$scope.names = store.getNames();

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
            }

            $scope.onLeaveSearch = function () {
                $timeout(function() {
                    $scope.showTable = false;
                }, 500);
            }

            $scope.nameClicked =  function (name) {
                globalVar.updateByName(name);
            }

            $scope.showTable = false;

        }])
        .config(function ($httpProvider) {
            delete $httpProvider.defaults.headers.common['X-Requested-With'];
        })
        // fake service, substitute with your server call ($http)
        .factory('store',function() {
            var names = ['Tomer', 'Omri', 'Avi', 'Vlad', 'Rotem', 'Micha', 'Jonny', 'Livne'];
            return {
                getNames : function(){
                    return names;
                },
            };
        });

    angular.bootstrap(document,['myApp']);

});