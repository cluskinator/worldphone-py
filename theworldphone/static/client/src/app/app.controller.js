(function() {
  'use strict';

  angular
    .module('worldphone')
    .controller('AppCtrl', AppCtrl);

  AppCtrl.$inject = ['$scope', '$state', 'auth', 'store', 'UserService', 'LanguageService'];

  function AppCtrl($scope, $state, auth, store, UserService, LanguageService) {
    $scope.auth = auth;

    $scope.logo = logo;
    $scope.login = login;
    $scope.logout = logout;
    $scope.year = new Date().getFullYear();

    $scope.$on('$stateChangeSuccess', stateChangeSuccess);

    function logo(authenticated) {
      $scope.expandedMenu = false;
      if (authenticated) {
        $state.go('profile');
      } else {
        $state.go('login');
      }
    };

    function login() {
      auth.signin({icon: '/assets/img/wp_logo_only.png'}, function (user, token) {
        // Success callback

        if (user.locale) { // Facebook
          user.location = user.locale.split('_')[1];
          user.nickname = auth.profile.name;
        }
        if (auth.profile.picture) {
          user.picture = auth.profile.picture;
          if (user.picture && user.picture.indexOf('cdn.auth0.com') > -1)
            user.picture = decodeURIComponent(user.picture).split('&d=')[1];
        }

        store.set('user', user);
        store.set('token', token);

        LanguageService.all(true); // Gets languages and saves them to local storage

        new UserService.resource(user).$query().then(function(response) {
          var details = response.data.attributes;

          user.uid = response.data.id;
          user.auth0_user_id = details.auth0_user_id;
          user.nickname = details.name;
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

          if (user.status == 'banned') {
            console.log("You don't have to go home, but you can't stay here.");
            $state.go('welcome');
            $scope.banned = true; // for pseudo flash
            logout();
          }

          if (user.status == 'new')
            $state.go('welcome');
          else
            $state.go('profile');
        });

      }, function(callback) {
        // Error callback
        console.log(callback);
      });
    };

    function logout() {
      console.log('See you next time!');
      auth.signout();
      store.remove('user');
      store.remove('token');
      store.remove('languages');
      $state.go('login');
    };

    function stateChangeSuccess(event, toState, toParams, fromState, fromParams) {
      if (angular.isDefined(toState.data.pageTitle)) {
        $scope.pageTitle = toState.data.pageTitle + ' | worldphone' ;
      }

      if (angular.isDefined(toState.data.loggedIn)) {
        $scope.loggedIn = toState.data.loggedIn;
      } else {
        $scope.loggedIn = false;
      }
      if (angular.isDefined(toState.data.inCall)) {
        $scope.inCall = toState.data.inCall;
      } else {
        $scope.inCall = false;
      }

      $scope.banned = false;
    };
  }

})();
