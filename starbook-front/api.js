angular.module('myApp')
  .factory('api', ['$http', '$timeout', 'ENV', '$cookies', function($http, $timeout, ENV, $cookies) {
    function addToken(query) {
      query['starbook-token'] = $cookies.get('starbook-token');
      return query;
    }

    return {
      get: function(query, callback) {
        var config = {
          withCredentials: ENV.SEND_COOKIES,
          headers: {
            'Content-Type': 'application/json'
          }
        };

        $timeout(function() {
          $http.post(ENV.STAR_BOOK_API, addToken({
            action: 'query',
            query: query,
            fields: ['boss', 'phone', 'title', 'hobbies', 'hood', 'name', 'expertise', 'email']
          }), config)
            .success(function(data, status, headers, config) {
              callback(data);
            })
            .error(function(data, status, header, config) {

            });
        });
      },
      tree: function() {
        return $http.post(ENV.STAR_BOOK_API, addToken({ action: 'tree' }), { withCredentials: ENV.SEND_COOKIES });
      },
      update: function(data) {
        data['action'] = 'update_person';
        return $http.post(ENV.STAR_BOOK_API, addToken(data), { withCredentials: ENV.SEND_COOKIES });
      },
      get_role: function() {
        return $http.post(ENV.STAR_BOOK_API, addToken({ action: 'get_role' }), { withCredentials: ENV.SEND_COOKIES });
      },
      remove_person: function(email) {
        return $http.post(ENV.STAR_BOOK_API, addToken({
          action: 'remove_person',
          email: email
        }), { withCredentials: ENV.SEND_COOKIES });
      },
      add_person: function(fields) {
        return $http.post(ENV.STAR_BOOK_API, addToken({
          action: 'add_person',
          email: fields.email.toLowerCase(),
          name: fields.name,
          boss: fields.boss.toLowerCase(),
          title: fields.title,
          hood: fields.hood,
          phone: fields.phone
        }), { withCredentials: ENV.SEND_COOKIES })
      }
    }
  }]);
  
