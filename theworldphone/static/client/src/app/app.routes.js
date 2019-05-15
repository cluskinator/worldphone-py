(function() {
  'use strict';

  angular
    .module('worldphone')
    .config(configureRoutes);

    function configureRoutes($stateProvider, $urlRouterProvider) {
      $urlRouterProvider.otherwise('/login');

      $stateProvider
        // .state('home', {
        //   url: '/home',
        //   templateUrl: '/templates/home/home.html',
        //   data: {
        //     pageTitle: 'Home',
        //   }
        // })

        .state('login', {
          url: '/login',
          templateUrl: '/templates/home/login.html',
          data: {
            pageTitle: 'Login',
          }
        })

        .state('welcome', {
          url: '/welcome',
          templateUrl: '/templates/profile/welcome.html',
          controller: 'ProfileCtrl',
          controllerAs: 'profile',
          data: {
            pageTitle: 'Welcome',
            requiresLogin: true,
          }
        })

        .state('call', {
          url: '/call',
          templateUrl: '/templates/call/call.html',
          controller: 'CallCtrl',
          controllerAs: 'call',
          data: {
            pageTitle: 'In Call',
            requiresLogin: true,
            inCall: true,
          },
          params: {
            callLanguages: { squash: true },
            callType: { squash: true }
          }
        })

        .state('callHistory', {
          url: '/call-history',
          templateUrl: '/templates/call-history/call-history.html',
          controller: 'CallHistoryCtrl',
          controllerAs: 'callHistory',
          data: {
            pageTitle: 'Call History',
            requiresLogin: true,
          }
        })

        .state('newCall', {
          url: '/new-call',
          templateUrl: '/templates/new-call/new-call.html',
          controller: 'NewCallCtrl',
          controllerAs: 'newCall',
          data: {
            pageTitle: 'New Call',
            requiresLogin: true,
          }
        })

        .state('profile', {
          url: '/profile',
          templateUrl: '/templates/profile/profile.html',
          controller: 'ProfileCtrl',
          controllerAs: 'profile',
          data: {
            pageTitle: 'Profile',
            requiresLogin: true,
          }
        })

        .state('about', {
          url: '/about',
          templateUrl: '/templates/home/about.html',
          data: {
            pageTitle: 'About',
          }
        })

        .state('faq', {
          url: '/faq',
          templateUrl: '/templates/home/faq.html',
          data: {
            pageTitle: 'FAQ',
          }
        })

        .state('privacy', {
          url: '/privacy',
          templateUrl: '/templates/home/privacy.html',
          data: {
            pageTitle: 'Privacy',
          }
        })

        .state('terms', {
          url: '/terms',
          templateUrl: '/templates/home/terms.html',
          data: {
            pageTitle: 'Terms',
          }
        });
    }

})();
