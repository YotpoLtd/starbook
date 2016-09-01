angular.module('myApp')
  .factory('api', ['$http', '$timeout', 'ENV', function($http, $timeout, ENV) {
    return {
      get: function(query, callback) {
        var config = {
          withCredentials: ENV.SEND_COOKIES,
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
      },
      update: function(data) {
        data['action'] = 'update_person';
        return $http.post(ENV.STAR_BOOK_API, data, { withCredentials: ENV.SEND_COOKIES });
      },
      get_role: function() {
        return $http.post(ENV.STAR_BOOK_API, { action: 'get_role' }, { withCredentials: ENV.SEND_COOKIES });
      },
      remove_person: function(email) {
        return $http.post(ENV.STAR_BOOK_API, {
          action: 'remove_person',
          email: email
        }, { withCredentials: ENV.SEND_COOKIES });
      }
    }
  }]);
  
