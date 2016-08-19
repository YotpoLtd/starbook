angular.module('myApp')
  .factory('elastic', ['$http', '$timeout', 'ENV', function($http, $timeout, ENV) {
    return {
      get: function(query, callback) {
        var config = {
          headers: {
            'Content-Type': 'application/json'
          }
        };

        $timeout(function() {
          $http.post(ENV.STAR_BOOK_API, { action: 'query', query: query }, config)
            .success(function(data, status, headers, config) {
              callback(data);
            })
            .error(function(data, status, header, config) {

            });
        });
      },
      tree: function() {
        return $http.post(ENV.STAR_BOOK_API, { action: 'tree' }, { withCredentials: ENV.SEND_COOKIES });
      }
    }
  }]);