angular.module('myApp')
  .factory('errorInterceptor', ['$q', '$injector', '$log',
  function($q, $injector, $log) {
    var preventInfiniteLoop = {};
    return {
      responseError: function(rejection) {
        switch (rejection.status) {
          case 401:
            var authService = $injector.get('authService');
            var $http = $injector.get('$http');
            var lastTry = preventInfiniteLoop[rejection.config.url];
            if (new Date() - lastTry < 10000) {
              return $q.reject(rejection);
            }
            return authService.retry().then(function() {
              preventInfiniteLoop[rejection.config.url] = new Date();
              return $http(rejection.config);
            }, function() {
              return $q.reject(rejection);
            });
            break;
          default:
            $log.error('Response error!');
            return $q.reject(rejection);
        }
      }
    };
  }])
  .config(['$httpProvider',function($httpProvider) {
    $httpProvider.interceptors.push('errorInterceptor');
  }]);