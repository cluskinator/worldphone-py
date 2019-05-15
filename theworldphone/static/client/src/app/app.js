(function() {
  'use strict';

  angular
    .module('worldphone', [
      'ui.router',
      'ngResource',
      'auth0',
      'angular-storage',
      'angular-jwt',
      'worldphone.user',
      'worldphone.call',
      'worldphone.callHistory',
      'worldphone.home',
      'worldphone.newCall',
      'worldphone.profile'
    ])
    .config(config)
    .run(run);

    function config($httpProvider, $resourceProvider, authProvider, jwtInterceptorProvider) {
      authProvider.init({
        domain: 'theworldphone.auth0.com',
        clientID: '4hsMGdHDV4AQSYjzXmFQGrHEYy7nw8D0',
        loginState: 'login'
      });

      // interceptor, fetches all requests and adds the jwt token to the authorization header.
      jwtInterceptorProvider.tokenGetter = function(store) {
        return store.get('token');
      };

      $httpProvider.interceptors.push('jwtInterceptor');

      $resourceProvider.defaults.stripTrailingSlashes = false;
    }

    function run($rootScope, auth, store, jwtHelper, $state, UserService) {
      // This hooks all auth events to check everything as soon as the app starts
      auth.hookEvents();

      // This event gets triggered on refresh or URL change
      $rootScope.$on('$locationChangeStart', function() {
        var token = store.get('token');
        if (!auth.isAuthenticated && token && !jwtHelper.isTokenExpired(token)) {
          auth.authenticate(store.get('user'), token);
        }
      });

      // Reload user data for profile page
      $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams, options) {
        if (auth.isAuthenticated) {
          var user = store.get('user');
          if (user && user.status == 'banned') {
            event.preventDefault();
            console.log("You don't have to go home, but you can't stay here.");
            // Basically just AppCtrl.logout()
            auth.signout();
            store.remove('user');
            store.remove('token');
            store.remove('languages');
            $state.go('login');
          }

          if (toState.name == 'profile') {
            new UserService.current();
          }

          if (toState.name == 'login') {
            console.log('You are already logged in.');
            $state.go(fromState.name);
          }

        } else {
          if (toState.data && toState.data.requiresLogin) {
            console.log('You must log in to access that page.');
            $state.go('login');
          }
        }
      });

      $rootScope.$on('$stateChangeSuccess', function() {
         document.body.scrollTop = document.documentElement.scrollTop = 0;
      });
    }

})();
