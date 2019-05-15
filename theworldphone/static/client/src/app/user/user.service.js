(function() {
  'use strict';

  angular
    .module('worldphone.user')
    .factory('LanguageService', LanguageService)
    .factory('UserService', UserService);

  LanguageService.$inject = ['$resource', 'store'];
  UserService.$inject = ['$resource', 'store', 'auth', 'LanguageService'];

  function LanguageService($resource, store) {
    var all = all;
    var has = has;

    return {
      all: all,
      has: has
    };

    function all(force) {
      var languages = store.get('languages') || [];
      if (force || !languages.length) {
        var resource = $resource('/api/v1/languages/');
        new resource().$get().then(function(response) {
          languages = response.data;
          store.set('languages', languages);
        });
      }
      return languages;
    }

    function has(languageName) {
      var languages = this.all();
      var languageNames = [];
      angular.forEach(languages, function(language) {
        languageNames.push(language.attributes.name);
      });
      return (languageNames.indexOf(languageName) != -1);
    }
  }

  function UserService($resource, store, auth, LanguageService) {
    var resource = $resource('/api/v1/users/:id',
      {id: '@user.id'},
      {
        query: {
          method: 'GET',
          url: '/api/v1/users/current/'
        },
        update: {
          method: 'PATCH',
        },
        rate: {
          method: 'PATCH',
          url: '/api/v1/users/:id/ratings'
        },
        languages: {
          method: 'PATCH',
          url: '/api/v1/users/:id/languages'
        },
        countries: {
          method: 'GET',
          url: '/api/v1/countries/'
        }
      }
    );

    var current = current;

    return {
      resource: resource,
      current: current
    };

    function current() {
      var user = store.get('user');
      new resource(user).$query().then(function(response) {
        var details = response.data.attributes;

        user.uid = response.data.id;
        user.auth0_user_id = details.auth0_user_id;
        user.gender = details.gender;
        user.location = details.location || user.location;
        user.status = details.status;
        user.spokenLanguages = details.spoken_languages.data;
        user.learningLanguages = details.learning_languages.data;
        if (details.ratings)
          user.ratings = details.ratings.data;
        else
          user.ratings = [];

        store.set('user', user);
        return user;
      });
    }
  }

})();
